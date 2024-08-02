import pandas as pd
import numpy as np
from lightfm import LightFM
from lightfm.data import Dataset
from lightfm.evaluation import precision_at_k, auc_score
import os

data_dir = "data"

# Paths to the data files
user_post_interactions_file = f'{data_dir}/user_post_interactions.csv'
post_details_file = f'{data_dir}/post_details.csv'
user_details_file = f'{data_dir}/user_details.csv'

# Load the data
def load_data():
    interactions = pd.read_csv(user_post_interactions_file)
    posts = pd.read_csv(post_details_file)
    users = pd.read_csv(user_details_file)
    return interactions, posts, users

# Prepare dataset for LightFM
def prepare_dataset(interactions, posts, users):
    dataset = Dataset()
    dataset.fit(
        users['user_id'],
        posts['post_id']
    )
    
    # Identify posts authored by each user
    authored_posts = posts.set_index('post_id')['user_id'].to_dict()
    
    # Filter out self-interactions for training
    interactions_filtered = interactions[interactions.apply(lambda x: authored_posts[x['post_id']] != x['user_id'], axis=1)]
    
    # Build interactions matrix
    (interactions_matrix, _) = dataset.build_interactions(
        [(row['user_id'], row['post_id']) for idx, row in interactions_filtered.iterrows()]
    )
    
    return dataset, interactions_matrix

# Train the LightFM model with metrics
def train_model(interactions_matrix, epochs=100):
    model = LightFM(loss='warp')
    for epoch in range(epochs):
        model.fit_partial(interactions_matrix, epochs=1, num_threads=8)
        
        # Calculate training metrics
        train_precision = precision_at_k(model, interactions_matrix, k=5).mean()
        train_auc = auc_score(model, interactions_matrix).mean()
        
        print(f"Epoch: {epoch+1}")
        print(f"Precision at k=5: {train_precision:.4f}")
        print(f"AUC Score: {train_auc:.4f}")
    return model

# Making recommendations and returning scores
def recommend(model, dataset, user_id, num_items=10):
    user_x = dataset.mapping()[0][user_id]
    all_item_ids = np.arange(dataset.interactions_shape()[1])
    scores = model.predict(user_x, all_item_ids)
    
    # Get top N item scores
    top_item_indices = np.argsort(-scores)[:num_items]
    top_item_scores = scores[top_item_indices]
    
    # Create a reverse mapping from index to item_id
    index_to_item_id = {v: k for k, v in dataset.mapping()[2].items()}
    
    # Get the top item IDs
    top_item_ids = [index_to_item_id[idx] for idx in top_item_indices]

    # Return list of tuples (post_id, score)
    return list(zip(top_item_ids, top_item_scores))

# Main execution
if __name__ == "__main__":
    interactions, posts, users = load_data()
    dataset, interactions_matrix = prepare_dataset(interactions, posts, users)
    model = train_model(interactions_matrix, epochs=300)
    
    # Example usage
    recommended_posts = recommend(model, dataset, 'pxnu33x7jtpx9ar1ytsi4yxbp6a5o36gwhffs8zoxmbuptici1jy')
    print(f"\nRecommended Post IDs and Scores for Ar: {recommended_posts}\n")

    recommended_posts = recommend(model, dataset, 'y4euc58gnmxun9wo87gwmanu6kztt9pgw1zz1yp1azp7trrsjamy')
    print(f"\nRecommended Post IDs and Scores for John Carvalho: {recommended_posts}\n")


    recommended_posts = recommend(model, dataset, '4snwyct86m383rsduhw5xgcxpw7c63j3pq8x4ycqikxgik8y64ro')
    print(f"\nRecommended Post IDs and Scores for Aldert: {recommended_posts}\n")