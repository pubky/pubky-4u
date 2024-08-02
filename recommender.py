import argparse
import pandas as pd
import numpy as np
from neo4j import GraphDatabase
from lightfm import LightFM
from lightfm.data import Dataset
from sklearn.preprocessing import MinMaxScaler

# Neo4j connection setup
uri = "bolt://localhost:7687"
username = "neo4j"
password = "12345678"
driver = GraphDatabase.driver(uri, auth=(username, password))

# Directory containing Cypher queries
query_dir = "queries"

# Paths to the data files
data_dir = "data"
user_post_interactions_file = f'{data_dir}/user_post_interactions.csv'
post_details_file = f'{data_dir}/post_details.csv'
user_details_file = f'{data_dir}/user_details.csv'

# Fetch web-of-trust scores from Neo4j
def fetch_web_of_trust_scores(user_id):
    with open(f"{query_dir}/wot_A.cypher", "r") as file:
        query = file.read()
    query = query.replace("{user_id}", user_id)

    with driver.session() as session:
        result = session.run(query)
        data = [{"post_id": record["post_id"], "WoT-Score": record["combined"]} for record in result]
    return pd.DataFrame(data)

# Normalize scores to the 0-1 range
def normalize_scores(df, score_col):
    scaler = MinMaxScaler()
    df[score_col] = scaler.fit_transform(df[[score_col]])
    return df

# Prepare LightFM model and compute scores
def compute_lightfm_scores(user_id, interactions, posts, users):
    dataset = Dataset()
    dataset.fit(users['user_id'], posts['post_id'])
    
    # Identify posts authored by each user
    authored_posts = posts.set_index('post_id')['user_id'].to_dict()
    
    # Filter out self-interactions for training
    interactions_filtered = interactions[interactions.apply(lambda x: authored_posts[x['post_id']] != x['user_id'], axis=1)]
    
    # Build interactions matrix
    (interactions_matrix, _) = dataset.build_interactions(
        [(row['user_id'], row['post_id']) for idx, row in interactions_filtered.iterrows()]
    )

    model = LightFM(loss='warp')
    model.fit(interactions_matrix, epochs=30, num_threads=8)
    
    user_x = dataset.mapping()[0][user_id]
    all_item_ids = np.arange(dataset.interactions_shape()[1])
    scores = model.predict(user_x, all_item_ids)
    
    index_to_item_id = {v: k for k, v in dataset.mapping()[2].items()}
    lightfm_scores = [{"post_id": index_to_item_id[idx], "ML-Score": score} for idx, score in enumerate(scores)]
    return pd.DataFrame(lightfm_scores)

# Main function to compute recommendations
def recommend_posts(user_id, weight, skip, limit):
    interactions, posts, users = load_data()
    wot_scores = fetch_web_of_trust_scores(user_id)
    wot_scores = normalize_scores(wot_scores, "WoT-Score")
    
    lightfm_scores = compute_lightfm_scores(user_id, interactions, posts, users)
    lightfm_scores = normalize_scores(lightfm_scores, "ML-Score")
    
    merged_scores = pd.merge(wot_scores, lightfm_scores, on="post_id", how="inner")
    merged_scores["Final-Score"] = (weight / 100) * merged_scores["ML-Score"] + ((100 - weight) / 100) * merged_scores["WoT-Score"]
    ranked_posts = merged_scores.sort_values(by="Final-Score", ascending=False).reset_index(drop=True)
    
    return ranked_posts[skip:skip+limit][["post_id", "Final-Score", "ML-Score", "WoT-Score"]]

# Load data from CSV files
def load_data():
    interactions = pd.read_csv(user_post_interactions_file)
    posts = pd.read_csv(post_details_file)
    users = pd.read_csv(user_details_file)
    return interactions, posts, users

# CLI argument parsing
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Recommend posts to a user based on Web-of-Trust and ML scores.")
    parser.add_argument("--user_id", type=str, required=True, help="The ID of the user to recommend posts for.")
    parser.add_argument("--weight", type=int, choices=range(0, 101), required=True, help="The weight to give to ML scores (0-100).")
    parser.add_argument("--skip", type=int, default=0, help="The number of posts to skip.")
    parser.add_argument("--limit", type=int, default=10, help="The number of posts to return.")
    
    args = parser.parse_args()
    
    recommended_posts = recommend_posts(args.user_id, args.weight, args.skip, args.limit)
    print(recommended_posts)
