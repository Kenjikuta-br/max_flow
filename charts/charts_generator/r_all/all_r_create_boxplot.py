import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import os

# Set style for better visuals
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

# 1. Load all CSV files
file_paths = [
    "results/iterations/basic_line/robust_results.csv",
    "results/iterations/matching/robust_results.csv",
    "results/iterations/random_2level/robust_results.csv",
    "results/iterations/square_mesh/robust_results.csv"
]

dfs = []
for path in file_paths:
    try:
        # Load CSV using semicolon as delimiter
        df = pd.read_csv(path, sep=';')
        
        # Extract graph type from path
        graph_type = path.split('/')[2]  # Adjusted index to match your path structure
        df['graph_type'] = graph_type
        dfs.append(df)
    except Exception as e:
        print(f"Error loading {path}: {str(e)}")
        continue

if not dfs:
    raise ValueError("No data files could be loaded.")

df = pd.concat(dfs, ignore_index=True)

# 2. Verify loaded data
print("\nFirst rows of combined DataFrame:")
print(df.head())
print("\nAvailable columns:")
print(df.columns.tolist())

# 3. Prepare data for visualization
algorithm_names = {
    'bfs': 'BFS',
    'dfs': 'DFS',
    'fat': 'Fattest',
    'scaling': 'Scaling'
}
df['algorithm'] = df['algorithm'].str.strip().str.lower().map(algorithm_names)

# 4. Create the visualization
plt.figure(figsize=(12, 8))

# Custom color palette
palette = {
    'BFS': '#1f77b4',
    'DFS': '#ff7f0e',
    'Fattest': '#2ca02c',
    'Scaling': '#d62728'
}

# Main boxplot
ax = sns.boxplot(
    x='algorithm',
    y='avg_r',
    data=df,
    palette=palette,
    showfliers=False,
    width=0.6,
    order=['BFS', 'DFS', 'Fattest', 'Scaling']
)

# Add individual data points
sns.stripplot(
    x='algorithm',
    y='avg_r',
    data=df,
    color='black',
    alpha=0.2,
    size=3,
    jitter=0.2
)

# Chart configuration
plt.yscale('log')
plt.title('Algorithm Iteration Efficiency (r) Comparison\nAll Graph Types Combined', 
          pad=20, fontsize=14, fontweight='bold')
plt.xlabel('Algorithm', labelpad=10, fontsize=12)
plt.ylabel('log(r) (lower is better)', labelpad=10, fontsize=12)

# Add median values
medians = df.groupby('algorithm')['avg_r'].median()
for i, algo in enumerate(['BFS', 'DFS', 'Fattest', 'Scaling']):
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

# Informative footer
plt.figtext(
    0.5, 0.01, 
    f"Combined data from {len(dfs)} graph types | Total {len(df)} observations", 
    ha='center', 
    fontsize=10, 
    color='gray'
)

plt.tight_layout()

# Save and show
os.makedirs('charts/r_all', exist_ok=True)
plt.savefig('charts/r_all/boxplot_r_all.png', bbox_inches='tight')
plt.show()

# 5. Descriptive statistics
print("\nDescriptive statistics by algorithm:")
print(df.groupby('algorithm')['avg_r'].describe().round(6))
