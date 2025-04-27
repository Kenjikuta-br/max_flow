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

dfs = []
for path in file_paths:
    try:
        # Read CSV
        df_part = pd.read_csv(path, sep=';')

        # Extract graph type from path
        graph_type = path.split('/')[2]
        df_part['graph_type'] = graph_type

        # Keep only necessary columns
        df_part = df_part[['graph_name', 'graph_type', 'algorithm', 'avg_s_bar', 'avg_t_bar_residual', 'avg_n']]

        dfs.append(df_part)
    except Exception as e:
        print(f"Error loading {path}: {str(e)}")
        continue

# 2. Combine all into a single DataFrame
if not dfs:
    raise ValueError("No files could be loaded.")

df = pd.concat(dfs, ignore_index=True)

# 3. Rename columns for clarity (English names)
df.rename(columns={
    'graph_name': 'graph_name',
    'graph_type': 'graph_type',
    'algorithm': 'algorithm',
    'avg_s_bar': 's_bar',        # defect of vertices
    'avg_t_bar_residual': 't_bar',  # defect of edges
    'avg_n': 'n_vertices'    # average number of vertices
}, inplace=True)

# 4. Clean 'algorithm' names (filter out 'fat', only BFS, DFS, Scaling)
df = df[df['algorithm'].isin(['bfs', 'dfs', 'scaling'])]

# 5. Create output folder
os.makedirs('charts/defect/scatter', exist_ok=True)

# 6. Scatter Plots for each dataset and each defect (s̄ and t̄)

for graph_type in df['graph_type'].unique():
    # Filter data by graph type
    graph_df = df[df['graph_type'] == graph_type]

    # 6.1. Scatter Plot 1: s̄ vs n_vertices with style by algorithm and hue by graph_type
    plt.figure(figsize=(10, 7))
    sns.scatterplot(
        data=graph_df,
        x='n_vertices',
        y='s_bar',
        hue='algorithm',  # Color by algorithm
        style='algorithm',  # Shape by algorithm
        palette='Set2',
        s=70,
        edgecolor='black'
    )
    plt.title(f's̄ (Defect of Vertices) vs Number of Vertices - {graph_type}', fontsize=16)
    plt.xlabel('Number of Vertices (n)', fontsize=13)
    plt.ylabel('s̄ (Defect of Vertices)', fontsize=13)
    plt.legend(title='Algorithm', bbox_to_anchor=(1.05, 1), loc='upper left')  # Legend for algorithm
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'charts/defect/scatter/s_bar_vs_vertices_{graph_type}.png', bbox_inches='tight')
    

    # 6.2. Scatter Plot 2: t̄ vs n_vertices with style by algorithm and hue by graph_type
    plt.figure(figsize=(10, 7))
    sns.scatterplot(
        data=graph_df,
        x='n_vertices',
        y='t_bar',
        hue='algorithm',  # Color by algorithm
        style='algorithm',  # Shape by algorithm
        palette='Set2',
        s=70,
        edgecolor='black'
    )
    plt.title(f't̄ (Defect of Edges) vs Number of Vertices - {graph_type}', fontsize=16)
    plt.xlabel('Number of Vertices (n)', fontsize=13)
    plt.ylabel('t̄ (Defect of Edges)', fontsize=13)
    plt.legend(title='Algorithm', bbox_to_anchor=(1.05, 1), loc='upper left')  # Legend for algorithm
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'charts/defect/scatter/t_bar_vs_vertices_{graph_type}.png', bbox_inches='tight')


# 7. Combine all datasets for a general view

# 7.1. Combined Scatter Plot: s̄ vs n_vertices for all datasets
plt.figure(figsize=(10, 7))
sns.scatterplot(
    data=df,
    x='n_vertices',
    y='s_bar',
    hue='graph_type',  # Color by graph type
    style='algorithm',  # Shape by algorithm
    palette='Set2',
    s=70,
    edgecolor='black'
)
plt.title('s̄ (Defect of Vertices) vs Number of Vertices - All Graph Types', fontsize=16)
plt.xlabel('Number of Vertices (n)', fontsize=13)
plt.ylabel('s̄ (Defect of Vertices)', fontsize=13)
plt.legend(title='Dataset', bbox_to_anchor=(1.05, 1), loc='upper left')  # Legend for graph type
plt.grid(True)
plt.tight_layout()
plt.savefig('charts/defect/scatter/s_bar_vs_vertices_all_graph_types.png', bbox_inches='tight')

# 7.2. Combined Scatter Plot: t̄ vs n_vertices for all datasets
plt.figure(figsize=(10, 7))
sns.scatterplot(
    data=df,
    x='n_vertices',
    y='t_bar',
    hue='graph_type',  # Color by graph type
    style='algorithm',  # Shape by algorithm
    palette='Set2',
    s=70,
    edgecolor='black'
)
plt.title('t̄ (Defect of Edges) vs Number of Vertices - All Graph Types', fontsize=16)
plt.xlabel('Number of Vertices (n)', fontsize=13)
plt.ylabel('t̄ (Defect of Edges)', fontsize=13)
plt.legend(title='Dataset', bbox_to_anchor=(1.05, 1), loc='upper left')  # Legend for graph type
plt.grid(True)
plt.tight_layout()
plt.savefig('charts/defect/scatter/t_bar_vs_vertices_all_graph_types.png', bbox_inches='tight')
