import time
from evaluate import evaluate_custom_alpha


def run_alpha_experiment(dataset_name, log_path, abs_values, rel_values, verbose=False):
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

    # --- Grid search for custom miner ---
    for abs_t in abs_values:
        for rel_t in rel_values:

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
            print(f"abs={abs_t}, rel={rel_t:.2f} → Custom F1={custom['f1']:.3f}")

    # --- Sort by F1 ---
    results_sorted = sorted(results, key=lambda r: r["f1"], reverse=True)
    best = results_sorted[0] if results_sorted else None

    if verbose:

        # --- Print summary ---
        print("\n=== GRID SEARCH RESULTS (sorted by Custom F1) ===")
        print(f"{'abs':>4} | {'rel':>4} | {'Precision':>10} | {'Recall':>10} | {'F1':>10}")
        print("-" * 50)
        for r in results_sorted:
            print(f"{r['abs']:>4} | {r['rel']:>4.1f} | {r['precision']:>10.3f} | {r['recall']:>10.3f} | {r['f1']:>10.3f}")


    print(f"\nBest configuration for {dataset_name}: abs={best['abs']}, rel={best['rel']}, F1={best['f1']:.3f}")
    elapsed = time.time() - start_time
    print(f"\nChecked {len(abs_values) * len(rel_values)} parameter combinations.")
    print(f"Execution time: {elapsed:.2f} seconds")

    return {
        "dataset": dataset_name,
        "results": results_sorted,
        "best": best,
        "elapsed": elapsed
    }


if __name__ == "__main__":

    ### Configuration ###
    dataset = "L1.xes"
    base_path = "data/"
    abs_values = [0,1,2,3]
    rel_values = [0.1,0.2,0.3]

    log_path = f"{base_path}{dataset}"
    result = run_alpha_experiment(dataset, log_path, abs_values, rel_values)


