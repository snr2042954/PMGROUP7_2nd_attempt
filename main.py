import os
from grid_search import run_alpha_experiment

# Configuration
DATA_FOLDER = "data/"
ABS_VALUES = [0,1,2,3,4]
REL_VALUES = [0.1,0.2,0.3,0.4]


def main():
    """
    Run Alpha Miner frequency experiments on all .xes logs in the folder.
    """

    # Detect all .xes files in the data folder
    xes_files = [
        f for f in os.listdir(DATA_FOLDER)
        if f.lower().endswith(".xes")
    ]

    print(f"Found {len(xes_files)} XES files:")
    for f in xes_files:
        print(f"  - {f}")

    all_results = []

    # Run experiment on each dataset
    for dataset in xes_files:
        dataset_path = os.path.join(DATA_FOLDER, dataset)
        result = run_alpha_experiment(dataset, dataset_path, ABS_VALUES, REL_VALUES)
        all_results.append(result)

    # Print summary of best F1 for all datasets
    print("\n============================")
    print(" SUMMARY OF BEST RESULTS ")
    print("============================")
    print(f"{'Dataset':<25} | {'Best F1':>7} | {'abs':>3} | {'rel':>3}")
    print("-" * 50)
    for res in all_results:
        best = res["best"]
        if best:
            print(f"{res['dataset']:<25} | {best['f1']:>7.3f} | {best['abs']:>3} | {best['rel']:>3.1f}")
        else:
            print(f"{res['dataset']:<25} | {'---':>7} | {'-':>3} | {'-':>3}")

    print("\nAll experiments complete.")


if __name__ == "__main__":
    main()
