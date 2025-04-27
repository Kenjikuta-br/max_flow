import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 1. Load CSVs
file_paths = [
    "results/iterations/basic_line/robust_results.csv",
    "results/iterations/matching/robust_results.csv",
    "results/iterations/random_2level/robust_results.csv",
    "results/iterations/square_mesh/robust_results.csv"
]

# Create output folder for each dataset
os.makedirs('charts/operation_counts', exist_ok=True)

# List to store all data for the combined plots (if needed later)
all_data = []

for path in file_paths:
    try:
        # Read CSV
        df = pd.read_csv(path, sep=';')

        # Extract graph type from path
        graph_type = path.split('/')[2]
        df['graph_type'] = graph_type

        # Keep only necessary columns
        df = df[['graph_name', 'graph_type', 'algorithm', 'avg_insert_norm', 'avg_delete_norm', 'avg_update_norm_m', 'avg_update_norm_theoretical', 'avg_iterations', 'avg_n']]

        # Rename columns for clarity (English names)
        df.rename(columns={
            'graph_name': 'graph_name',
            'graph_type': 'graph_type',
            'algorithm': 'algorithm',
            'avg_insert_norm': 'insert',
            'avg_delete_norm': 'delete',
            'avg_update_norm_m': 'update_m',
            'avg_update_norm_theoretical': 'update_theoretical',
            'avg_iterations': 'iterations',
            'avg_n': 'vertices'
        }, inplace=True)

        # Filter only 'fat' algorithm
        df = df[df['algorithm'] == 'fat']

        # Create a plot with iterations on the X-axis
        sns.set_style("whitegrid")
        plt.figure(figsize=(10, 7))

        # Plot the data for insert, delete, update (m) and update (theoretical) vs iterations
        sns.lineplot(data=df, x='iterations', y='insert', label='Insert', marker='o', color='blue', linewidth=2)
        sns.lineplot(data=df, x='iterations', y='delete', label='Delete', marker='o', color='red', linewidth=2)
        sns.lineplot(data=df, x='iterations', y='update_m', label='Update (m)', marker='o', color='green', linewidth=2)
        sns.lineplot(data=df, x='iterations', y='update_theoretical', label='Update (Theoretical)', marker='o', color='purple', linewidth=2)

        plt.title(f'Operation Counts for Fat Algorithm ({graph_type}) - Iterations vs Operations', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Number of Iterations', fontsize=13)
        plt.ylabel('Operation Count (Normalized)', fontsize=13)
        plt.legend(title='Operation Type', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True)

        # Save plot for this dataset (Iterations on X)
        plt.tight_layout()
        plt.savefig(f'charts/operation_counts/operation_counts_fat_{graph_type}_iterations.png', bbox_inches='tight')
        plt.close()  # Close the plot to save memory

        # Create a plot with vertices on the X-axis
        plt.figure(figsize=(10, 7))

        # Plot the data for insert, delete, update (m) and update (theoretical) vs vertices
        sns.lineplot(data=df, x='vertices', y='insert', label='Insert', marker='o', color='blue', linewidth=2)
        sns.lineplot(data=df, x='vertices', y='delete', label='Delete', marker='o', color='red', linewidth=2)
        sns.lineplot(data=df, x='vertices', y='update_m', label='Update (m)', marker='o', color='green', linewidth=2)
        sns.lineplot(data=df, x='vertices', y='update_theoretical', label='Update (Theoretical)', marker='o', color='purple', linewidth=2)

        plt.title(f'Operation Counts for Fat Algorithm ({graph_type}) - Vertices vs Operations', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Number of Vertices', fontsize=13)
        plt.ylabel('Operation Count (Normalized)', fontsize=13)
        plt.legend(title='Operation Type', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True)

        # Save plot for this dataset (Vertices on X)
        plt.tight_layout()
        plt.savefig(f'charts/operation_counts/operation_counts_fat_{graph_type}_vertices.png', bbox_inches='tight')
        plt.close()  # Close the plot to save memory

        # Append to all data for combined dataset plots (if needed later)
        all_data.append(df)

    except Exception as e:
        print(f"Error loading {path}: {str(e)}")
        continue

print("All plots for individual datasets have been saved.")
