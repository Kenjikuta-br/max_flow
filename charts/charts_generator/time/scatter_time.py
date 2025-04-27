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

        # Extract graph type from the path
        graph_type = path.split('/')[2]
        df_part['graph_type'] = graph_type

        # Keep only necessary columns
        df_part = df_part[['graph_name', 'graph_type', 'algorithm', 'avg_n', 'avg_runtime', 'avg_time_per_mI', 'avg_time_over_nm', 'avg_time_per_nI', 'avg_time_over_I_sntm']] 

        dfs.append(df_part)
    except Exception as e:
        print(f"Error loading {path}: {str(e)}")
        continue

# 2. Combine all datasets into a single DataFrame
if not dfs:
    raise ValueError("No files could be loaded.")

df = pd.concat(dfs, ignore_index=True)

# 3. Rename columns for clarity
df.rename(columns={
    'graph_name': 'graph_name',
    'graph_type': 'graph_type',
    'algorithm': 'algorithm',
    'avg_n': 'n_vertices',    # Average number of vertices
    'avg_runtime': 'total_runtime',  # Time to be used in the plot
    'avg_time_per_mI': 'time_per_mI',  
    'avg_time_over_nm': 'time_over_nm',
    'avg_time_per_nI': 'time_per_nI',
    'avg_time_over_I_sntm': 'time_over_I_sntm'
}, inplace=True)

# 4. Create output folders for each parameter
output_dirs = {
    'total_runtime': 'charts/time/scatter/runtime',
    'time_per_mI': 'charts/time/scatter/time_per_mI',
    'time_per_nI': 'charts/time/scatter/time_per_nI',
    'time_over_nm': 'charts/time/scatter/time_over_nm',
    'time_over_I_sntm': 'charts/time/scatter/time_over_I_sntm'
}

for folder in output_dirs.values():
    os.makedirs(folder, exist_ok=True)

# 5. Define the parameters and graph types
parameters = ['total_runtime', 'time_per_mI', 'time_per_nI', 'time_over_nm', 'time_over_I_sntm']
graph_types = ['basic_line', 'matching', 'random_2level', 'square_mesh']

# 6. Generate a separate plot for each parameter and graph type
for param in parameters:
    for graph_type in graph_types:
        plt.figure(figsize=(10, 6))

        # Filter data for the current graph type
        df_graph_type = df[df['graph_type'] == graph_type]

        # Define a color palette for the algorithms
        palette = sns.color_palette("Set1", n_colors=df_graph_type['algorithm'].nunique())

        # Create line plots for each algorithm
        sns.lineplot(
            data=df_graph_type,
            x='n_vertices',
            y=param,
            hue='algorithm',  # Separate lines for each algorithm
            style='algorithm',  # Different line styles for each algorithm
            markers=True,  # Markers at data points
            palette=palette  # Use the defined color palette
        )

        # 7. Configure the plot
        plt.title(f'{param} vs Number of Vertices for {graph_type} Graph', fontsize=16)
        plt.xlabel('Number of Vertices', fontsize=13)
        plt.ylabel(f'{param} (miliseconds)', fontsize=13)
        plt.legend(title='Algorithm', loc='upper left')
        plt.grid(True)
        plt.tight_layout()

        # 8. Save the plot in the corresponding folder
        plt.savefig(f'{output_dirs[param]}/total_{param}_vs_vertices_{graph_type}.png', bbox_inches='tight')
