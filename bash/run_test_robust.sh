#!/usr/bin/env bash
set -euo pipefail

# ==== CONFIG ====
GRAPHS_DIR="./graphs"                     # folder with your .dimacs graphs
MY_EXE="./bin/robust_test"                # your benchmarking executable
OUTPUT_DIR="results/iterations"
OUTPUT_CSV="$OUTPUT_DIR/robust_results.csv"

# ==== PREPARE OUTPUT ====
mkdir -p "$OUTPUT_DIR"

# multi-line here-doc for readability, but collapse into one line in the file
cat <<'EOF' | tr -d '\n' > "$OUTPUT_CSV"
graph;algorithm;max_flow;avg_runtime;avg_iterations;avg_bound;avg_r;avg_m;avg_cFrac;avg_rBar;
avg_time_per_mI;avg_time_per_nI;avg_time_over_nm_n_plus_m;avg_time_over_r_2nm_sntm;avg_time_over_I_sntm;
avg_s_bar;avg_t_bar_forward;avg_t_bar_residual;avg_insert_norm;avg_delete_norm;avg_update_norm_m;avg_update_norm_theoretical
EOF

printf '\n' >> "$OUTPUT_CSV"

# ==== CHECK EXECUTABLE ====
if [[ ! -x "$MY_EXE" ]]; then
  echo "❌ Error: executable '$MY_EXE' not found or not executable." >&2
  exit 1
fi

# ==== RUN BENCHMARKS ====
for graph in "$GRAPHS_DIR"/*.dimacs; do
  [[ -e "$graph" ]] || continue   # skip if no .dimacs files

  base=$(basename "$graph")

  # Pipe graph into the tester, prefix each line with graph name, 
  # then convert all commas to semicolons for a uniform delimiter
  "$MY_EXE" < "$graph" \
    | sed -e "s/^/${base};/" -e "s/,/;/g" \
    >> "$OUTPUT_CSV"
done

echo "✅ Benchmark complete. Results written to '$OUTPUT_CSV'"
