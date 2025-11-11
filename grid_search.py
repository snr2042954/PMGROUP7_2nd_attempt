import time
from evaluate import evaluate_pm4py_alpha, evaluate_custom_alpha


def run_alpha_experiment(dataset_name, log_path, abs_values, rel_values):
    """
    Run grid search experiment for one dataset.

    Parameters:
        dataset_name (str): Name of the dataset (for printing/logging).
        log_path (str): Path to the .xes log file.
        abs_values (list[int]): Absolute threshold values.
        rel_values (list[float]): Relative threshold values.

    Returns:
        dict: Best result and all results sorted by F1 score.
    """
    print(f"\n=== Running experiment for {dataset_name} ===")
    start_time = time.time()

    results = []

    # --- Run PM4Py baseline once ---
    print("Running PM4Py Alpha Miner once for baseline...")
    pm4py_results = evaluate_pm4py_alpha(dataset_name, log_path)
    print(f"Baseline PM4Py F1: {pm4py_results['f1']:.3f}\n")

    # --- Grid search for custom miner ---
    for abs_t in abs_values:
        for rel_t in rel_values:
            try:
                custom = evaluate_custom_alpha(dataset_name, log_path,
                                               abs_threshold=abs_t,
                                               rel_threshold=rel_t)
                results.append({
                    "abs": abs_t,
                    "rel": rel_t,
                    "precision": custom["precision"],
                    "recall": custom["recall"],
                    "f1": custom["f1"],
                })
                print(f"abs={abs_t}, rel={rel_t:.1f} → Custom F1={custom['f1']:.3f}")
            except Exception as e:
                print(f"⚠️ Error at abs={abs_t}, rel={rel_t}: {e}")

    # --- Sort by F1 ---
    results_sorted = sorted(results, key=lambda r: r["f1"], reverse=True)
    best = results_sorted[0] if results_sorted else None

    # --- Print summary ---
    print("\n=== GRID SEARCH RESULTS (sorted by Custom F1) ===")
    print(f"{'abs':>4} | {'rel':>4} | {'Precision':>10} | {'Recall':>10} | {'F1':>10}")
    print("-" * 50)
    for r in results_sorted:
        print(f"{r['abs']:>4} | {r['rel']:>4.1f} | {r['precision']:>10.3f} | {r['recall']:>10.3f} | {r['f1']:>10.3f}")

    elapsed = time.time() - start_time
    print(f"\nChecked {len(abs_values) * len(rel_values)} parameter combinations.")
    print(f"Execution time: {elapsed:.2f} seconds")

    if best:
        print(f"\nBest configuration for {dataset_name}: abs={best['abs']}, rel={best['rel']}, F1={best['f1']:.3f}")
    else:
        print(f"\nNo valid results for {dataset_name}.")

    return {
        "dataset": dataset_name,
        "baseline": pm4py_results,
        "results": results_sorted,
        "best": best,
        "elapsed": elapsed
    }


if __name__ == "__main__":

    ### Configuration ###
    dataset = "L1.xes"
    base_path = "data/"
    abs_values = [0,1,2,3,4,5,6,7,8,9]
    rel_values = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]

    log_path = f"{base_path}{dataset}"
    result = run_alpha_experiment(dataset, log_path, abs_values, rel_values)


