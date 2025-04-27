import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set style for better visuals
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

# 1. Load all CSV files
file_paths = [
    "results/iterations_copy/basic_line/robust_results.csv",
    "results/iterations_copy/matching/robust_results.csv",
    "results/iterations_copy/random_2level/robust_results.csv",
    "results/iterations_copy/square_mesh/robust_results.csv"
]

dfs = []
for path in file_paths:
    try:
        df = pd.read_csv(path, sep=';')
        graph_type = path.split('/')[2]  # Extract graph type from path
        df['graph_type'] = graph_type
        dfs.append(df)
    except Exception as e:
        print(f"Error loading {path}: {str(e)}")
        continue

if not dfs:
    raise ValueError("No data files could be loaded.")

# Combine for full analysis
full_df = pd.concat(dfs, ignore_index=True)

# Normalize algorithm names
algorithm_names = {
    'bfs': 'BFS',
    'dfs': 'DFS',
    'fat': 'Fattest',
    'scaling': 'Scaling'
}
full_df['algorithm'] = full_df['algorithm'].str.strip().str.lower().map(algorithm_names)

# 2. Create folder to save charts
os.makedirs('charts/r_by_graph_type', exist_ok=True)

# 3. Generate one plot per graph_type
for graph_type, df_group in full_df.groupby('graph_type'):

    plt.figure(figsize=(12, 8))

    palette = {
        'BFS': '#1f77b4',
        'DFS': '#ff7f0e',
        'Fattest': '#2ca02c',
        'Scaling': '#d62728'
    }

    ax = sns.boxplot(
        x='algorithm',
        y='avg_r',
        data=df_group,
        palette=palette,
        showfliers=False,
        width=0.6,
        order=['BFS', 'DFS', 'Fattest', 'Scaling']
    )

    sns.stripplot(
        x='algorithm',
        y='avg_r',
        data=df_group,
        color='black',
        alpha=0.2,
        size=3,
        jitter=0.2
    )

    plt.yscale('log')
    plt.title(f'Algorithm Iteration Efficiency (r) - {graph_type.capitalize()}', 
              pad=20, fontsize=14, fontweight='bold')
    plt.xlabel('Algorithm', labelpad=10, fontsize=12)
    plt.ylabel('log(r) (lower is better)', labelpad=10, fontsize=12)

    # Medians
    medians = df_group.groupby('algorithm')['avg_r'].median()
    for i, algo in enumerate(['BFS', 'DFS', 'Fattest', 'Scaling']):
        if algo in medians.index:
            ax.text(
                i,
                medians[algo],
                f'Median:\n{medians[algo]:.2e}',
                ha='center',
                va='center',
                color='white',
                fontweight='bold',
                fontsize=9,
                bbox=dict(facecolor='black', alpha=0.7, boxstyle='round,pad=0.3')
            )

    plt.figtext(
        0.5, 0.01,
        f"Data from {graph_type} graph type | {len(df_group)} observations",
        ha='center',
        fontsize=10,
        color='gray'
    )

    plt.tight_layout()

    # Save plot
    plt.savefig(f'charts/r_by_graph_type/boxplot_r_{graph_type}.png', bbox_inches='tight')
    plt.close()

print("\nFinished generating all individual graph type boxplots!")
