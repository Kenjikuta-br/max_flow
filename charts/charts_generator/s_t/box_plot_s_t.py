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
os.makedirs('charts/defect/boxplots/algorithms', exist_ok=True)

# 6. Box plots for all algorithms combined
# 6.1. Box plot for s̄ (Defect of Vertices) by Graph Type and Algorithm
plt.figure(figsize=(10, 7))
sns.boxplot(
    data=df,
    x='graph_type',  # X-axis: graph type
    y='s_bar',       # Y-axis: defect of vertices
    hue='algorithm',  # Color by algorithm
    palette='Set2'
)
plt.title('Box Plot: Defect of Vertices (s̄) by Graph Type and Algorithm', fontsize=16)
plt.xlabel('Graph Type', fontsize=13)
plt.ylabel('Defect of Vertices (s̄)', fontsize=13)
plt.legend(title='Algorithm', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.tight_layout()
plt.savefig('charts/defect/boxplots/s_bar_by_graph_and_algorithm.png', bbox_inches='tight')

# 6.2. Box plot for t̄ (Defect of Edges) by Graph Type and Algorithm
plt.figure(figsize=(10, 7))
sns.boxplot(
    data=df,
    x='graph_type',  # X-axis: graph type
    y='t_bar',       # Y-axis: defect of edges
    hue='algorithm',  # Color by algorithm
    palette='Set2'
)
plt.title('Box Plot: Defect of Edges (t̄) by Graph Type and Algorithm', fontsize=16)
plt.xlabel('Graph Type', fontsize=13)
plt.ylabel('Defect of Edges (t̄)', fontsize=13)
plt.legend(title='Algorithm', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.tight_layout()
plt.savefig('charts/defect/boxplots/t_bar_by_graph_and_algorithm.png', bbox_inches='tight')

# 7. Box plots for each algorithm (BFS, DFS, Scaling)
algorithms = ['bfs', 'dfs', 'scaling']

for algo in algorithms:
    # Filter the DataFrame by the specific algorithm
    df_algo = df[df['algorithm'] == algo]

    # 7.1. Box plot for s̄ (Defect of Vertices) by Graph Type and Algorithm
    plt.figure(figsize=(10, 7))
    sns.boxplot(
        data=df_algo,
        x='graph_type',  # X-axis: graph type
        y='s_bar',       # Y-axis: defect of vertices
        palette='Set2'
    )
    plt.title(f'Box Plot: Defect of Vertices (s̄) by Graph Type - {algo.upper()}', fontsize=16)
    plt.xlabel('Graph Type', fontsize=13)
    plt.ylabel('Defect of Vertices (s̄)', fontsize=13)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'charts/defect/boxplots/algorithms/s_bar_by_graph_and_{algo}.png', bbox_inches='tight')

    # 7.2. Box plot for t̄ (Defect of Edges) by Graph Type and Algorithm
    plt.figure(figsize=(10, 7))
    sns.boxplot(
        data=df_algo,
        x='graph_type',  # X-axis: graph type
        y='t_bar',       # Y-axis: defect of edges
        palette='Set2'
    )
    plt.title(f'Box Plot: Defect of Edges (t̄) by Graph Type - {algo.upper()}', fontsize=16)
    plt.xlabel('Graph Type', fontsize=13)
    plt.ylabel('Defect of Edges (t̄)', fontsize=13)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'charts/defect/boxplots/algorithms/t_bar_by_graph_and_{algo}.png', bbox_inches='tight')
