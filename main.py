# main.py

import os

from evaluate import (
    evaluate_pm4py_alpha,
    evaluate_pm4py_heuristics,
    evaluate_custom_alpha
)
from grid_search import run_alpha_experiment
from alpha_miner import AlphaMinerFrequencies
from visualize import visualize_model
from utils.gold_standards import standards



def run_full_analysis_for_dataset(dataset: str, abs_values: list[int], rel_values: list[float]):
    print(f"\n\n============================")
    print(f"Dataset: {dataset}")
    print("============================")

    log_path = f"data/{dataset}"

    ### 1. first do a Grid search
    search_results = run_alpha_experiment(dataset, log_path, abs_values, rel_values)
    best = search_results["best"]
    abs_best = best["abs"]
    rel_best = best["rel"]

    ### 2. Summarize all different results
    best_result = evaluate_custom_alpha(dataset, log_path, abs_best, rel_best)
    default_result = evaluate_custom_alpha(dataset, log_path, abs_threshold=0, rel_threshold=0.0)
    alpha_result = evaluate_pm4py_alpha(dataset, log_path)
    heuristics_result = evaluate_pm4py_heuristics(dataset, log_path)

    # Summary
    print(f"\n📊 === Evaluation Summary for {dataset} ===")
    print(f"→ Gold standard relations: {len(standards[dataset].direct_succession)}")
    print(f"→ Best config: abs={abs_best}, rel={rel_best:.1f}")
    print("\n--- Best Custom Miner ---")
    print(f"Precision: {best_result['precision']:.3f}")
    print(f"Recall:    {best_result['recall']:.3f}")
    print(f"F1 Score:  {best_result['f1']:.3f}")

    print("\n--- Default (0, 0) Custom Miner ---")
    print(f"Precision: {default_result['precision']:.3f}")
    print(f"Recall:    {default_result['recall']:.3f}")
    print(f"F1 Score:  {default_result['f1']:.3f}")

    print("\n--- PM4Py Alpha Miner ---")
    print(f"Precision: {alpha_result['precision']:.3f}")
    print(f"Recall:    {alpha_result['recall']:.3f}")
    print(f"F1 Score:  {alpha_result['f1']:.3f}")

    print("\n--- PM4Py Heuristics Miner ---")
    print(f"Precision: {heuristics_result['precision']:.3f}")
    print(f"Recall:    {heuristics_result['recall']:.3f}")
    print(f"F1 Score:  {heuristics_result['f1']:.3f}")

    # Visualize best model
    miner = AlphaMinerFrequencies(abs_best, rel_best)
    miner.run(log_path)
    output_file = f"outputs/{dataset.replace('.xes', '')}_best_model"
    visualize_model(miner, output_file)



if __name__ == "__main__":

    abs_values = [1, 2, 3, 4, 5]
    rel_values = [0, 0.1, 0.2, 0.3, 0.4, 0.5]

    os.makedirs("outputs", exist_ok=True)

    datasets = list(standards.keys())

    for dataset in datasets:
        run_full_analysis_for_dataset(dataset, abs_values, rel_values)

    #run_full_analysis_for_dataset('BPI_Challenge_2012.xes', abs_values, rel_values)

    print("\n\n🎉 All datasets processed successfully.")
