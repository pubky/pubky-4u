import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
import os

warnings.filterwarnings('ignore', category=FutureWarning)

data_dir = "data"
plot_dir = 'plots'

os.makedirs(plot_dir, exist_ok=True)

# Load data
interactions = pd.read_csv(f'{data_dir}/user_post_interactions.csv')
posts = pd.read_csv(f'{data_dir}/post_details.csv')
users = pd.read_csv(f'{data_dir}/user_details.csv')

# Function to print dataframe statistics
def print_statistics(df, df_name):
    print(f"\nStatistics for {df_name}:")
    print(df.describe(include='all'))
    print("\nMissing values:")
    print(df.isnull().sum())

# Print statistics for each dataframe
print_statistics(interactions, "User-Post Interactions")
print_statistics(posts, "Post Details")
print_statistics(users, "User Details")

# Visualization of data
def plot_data(df, df_name):
    print(f"\nVisualizing and saving plots for {df_name}")
    for column in df.select_dtypes(include=['number']).columns:
        plt.figure(figsize=(10, 4))
        sns.histplot(df[column].dropna(), kde=True)
        plt.title(f'Distribution of {column} in {df_name}')
        # Save the plot instead of showing it
        plt.savefig(os.path.join(plot_dir, f'{df_name}_{column}.png'))
        plt.close()  # Close the plot to free up memory

    if 'interaction_type' in df.columns:
        plt.figure(figsize=(10, 4))
        sns.countplot(data=df, x='interaction_type')
        plt.title('Count of Interaction Types in User-Post Interactions')
        # Save the plot instead of showing it
        plt.savefig(os.path.join(plot_dir, f'{df_name}_interaction_types.png'))
        plt.close()  # Close the plot to free up memory

# Example usage (Assuming print_statistics is called elsewhere)
plot_data(interactions, "User-Post Interactions")
plot_data(posts, "Post Details")
plot_data(users, "User Details")
