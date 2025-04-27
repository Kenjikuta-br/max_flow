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
os.makedirs('charts/criticality', exist_ok=True)

# List to store all data for the combined plots
all_data = []

for path in file_paths:
    try:
        # Read CSV
        df = pd.read_csv(path, sep=';')

        # Extract graph type from path
        graph_type = path.split('/')[2]
        df['graph_type'] = graph_type

        # Keep only necessary columns
        df = df[['graph_name', 'graph_type', 'algorithm', 'avg_cFrac', 'avg_rBar', 'avg_n']]

        # Rename columns for clarity (English names)
        df.rename(columns={
            'graph_name': 'graph_name',
            'graph_type': 'graph_type',
            'algorithm': 'algorithm',
            'avg_cFrac': 'C',        # fraction of critical arcs
            'avg_rBar': 'r_mean',    # average criticality
            'avg_n': 'n_vertices'    # average number of vertices
        }, inplace=True)

        # Clean 'algorithm' names and filter for 'BFS' only
        algorithm_mapping = {
            'bfs': 'BFS',
            'dfs': 'DFS',
            'fat': 'Fattest',
            'scaling': 'Scaling'
        }
        df['algorithm'] = df['algorithm'].str.strip().str.lower().map(algorithm_mapping)

        # Filtrar somente 'BFS'
        df = df[df['algorithm'] == 'BFS']

        # 7. Scatter Plot 1: r_mean vs n_vertices (for current dataset)
        sns.set_style("whitegrid")
        plt.figure(figsize=(10, 7))

        scatter1 = sns.scatterplot(
            data=df,
            x='n_vertices',
            y='r_mean',
            hue='graph_type',
            style='graph_type',
            palette='Set2',
            s=70,
            edgecolor='black'
        )

        plt.title(f'Average Criticality vs Number of Vertices ({graph_type})', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Number of Vertices (n)', fontsize=13)
        plt.ylabel('r̄ (Average Criticality)', fontsize=13)
        plt.legend(title='Graph Type', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True)

        # Save plot for this dataset
        plt.tight_layout()
        plt.savefig(f'charts/criticality/r_mean_vs_vertices_{graph_type}.png', bbox_inches='tight')
        plt.close()  # Close the plot to save memory

        # 8. Scatter Plot 2: C vs n_vertices (for current dataset)
        plt.figure(figsize=(10, 7))

        scatter2 = sns.scatterplot(
            data=df,
            x='n_vertices',
            y='C',
            hue='graph_type',
            style='graph_type',
            palette='Set2',
            s=70,
            edgecolor='black'
        )

        plt.title(f'Fraction of Critical Edges vs Number of Vertices ({graph_type})', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Number of Vertices (n)', fontsize=13)
        plt.ylabel('C (Fraction of Critical Edges)', fontsize=13)
        plt.legend(title='Graph Type', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True)

        # Save plot for this dataset
        plt.tight_layout()
        plt.savefig(f'charts/criticality/c_frac_vs_vertices_{graph_type}.png', bbox_inches='tight')
        plt.close()  # Close the plot to save memory

        # Append to all data for combined dataset plots
        all_data.append(df)

    except Exception as e:
        print(f"Error loading {path}: {str(e)}")
        continue

# Combine all datasets for global plots
combined_df = pd.concat(all_data, ignore_index=True)

# 9. Combined Scatter Plot 1: r_mean vs n_vertices (all datasets)
plt.figure(figsize=(10, 7))

scatter_combined1 = sns.scatterplot(
    data=combined_df,
    x='n_vertices',
    y='r_mean',
    hue='graph_type',
    style='graph_type',
    palette='Set2',
    s=70,
    edgecolor='black'
)

plt.title('Average Criticality vs Number of Vertices (All Datasets)', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Number of Vertices (n)', fontsize=13)
plt.ylabel('r̄ (Average Criticality)', fontsize=13)
plt.legend(title='Graph Type', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)

# Save plot for all datasets
plt.tight_layout()
plt.savefig('charts/criticality/r_mean_vs_vertices_all.png', bbox_inches='tight')
plt.close()

# 10. Combined Scatter Plot 2: C vs n_vertices (all datasets)
plt.figure(figsize=(10, 7))

scatter_combined2 = sns.scatterplot(
    data=combined_df,
    x='n_vertices',
    y='C',
    hue='graph_type',
    style='graph_type',
    palette='Set2',
    s=70,
    edgecolor='black'
)

plt.title('Fraction of Critical Edges vs Number of Vertices (All Datasets)', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Number of Vertices (n)', fontsize=13)
plt.ylabel('C (Fraction of Critical Edges)', fontsize=13)
plt.legend(title='Graph Type', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)

# Save plot for all datasets
plt.tight_layout()
plt.savefig('charts/criticality/c_frac_vs_vertices_all.png', bbox_inches='tight')
plt.close()

print("All plots have been saved.")
