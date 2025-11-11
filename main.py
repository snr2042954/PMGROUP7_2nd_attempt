import os
import yaml

from evaluate import (
    evaluate_pm4py_alpha,
    evaluate_pm4py_heuristics,
    evaluate_custom_alpha
)
from grid_search import run_alpha_experiment
from alpha_miner import AlphaMinerFrequencies
from visualize import visualize_model
from utils.gold_standards import standards
from generate_html_from_yaml import generate_html_from_yaml
from visualize_gold_standards import visualize_all_gold_standards

def to_serializable(obj):
    """Helper function for export_results_to_yaml"""
    if isinstance(obj, tuple):
        return list(obj)
    if isinstance(obj, list):
        return [to_serializable(x) for x in obj]
    if isinstance(obj, dict):
        return {k: to_serializable(v) for k, v in obj.items()}
    return obj

def export_results_to_yaml(dataset, search_results, best_result, default_result,
                           alpha_result, heuristics_result, miner):
    """Save experiment results and model configuration to a YAML file."""

    file_path = f"outputs/yamls/{dataset.replace('.xes', '')}_results.yaml"

    export_data = {
        "dataset": dataset,
        "best_parameters": {
            "abs_threshold": search_results["best"]["abs"],
            "rel_threshold": search_results["best"]["rel"],
            "f1": search_results["best"]["f1"],
        },
        "top_10_combinations": search_results["results"][:10],
        "evaluation_custom": {
            "precision": best_result["precision"],
            "recall": best_result["recall"],
            "f1": best_result["f1"],
            "tp": best_result["tp"],
            "fp": best_result["fp"],
            "fn": best_result["fn"],
            "tn": best_result["tn"],
        },
        "evaluation_default": {
            "precision": default_result["precision"],
            "recall": default_result["recall"],
            "f1": default_result["f1"],
            "tp": default_result["tp"],
            "fp": default_result["fp"],
            "fn": default_result["fn"],
            "tn": default_result["tn"],
        },
        "evaluation_alpha": {
            "precision": alpha_result["precision"],
            "recall": alpha_result["recall"],
            "f1": alpha_result["f1"],
            "tp": alpha_result["tp"],
            "fp": alpha_result["fp"],
            "fn": alpha_result["fn"],
            "tn": alpha_result["tn"],
        },
        "evaluation_heuristic": {
            "precision": heuristics_result["precision"],
            "recall": heuristics_result["recall"],
            "f1": heuristics_result["f1"],
            "tp": heuristics_result["tp"],
            "fp": heuristics_result["fp"],
            "fn": heuristics_result["fn"],
            "tn": heuristics_result["tn"],
        },
        "relations_found": list(map(list, best_result["relations"])),
        "configured_net": {
            "places": miner.P_w,
            "transitions": miner.T_w,
            "flows": miner.F_w,
            "parallel": miner.parallel,
            "causality": miner.causality,
        },
    }

    with open(file_path, "w") as f:
        yaml.safe_dump(to_serializable(export_data), f, sort_keys=False)

    print(f"Exported results for {dataset} to {file_path}")

def run_full_analysis_for_dataset(dataset: str, abs_values: list[int], rel_values: list[float], verbose: bool = True):
    print(f"\n\n============================")
    print(f"Dataset: {dataset}")
    print("============================")

    log_path = f"data/{dataset}"

    ### 1. first do a Grid search
    search_results = run_alpha_experiment(dataset, log_path, abs_values, rel_values)
    best = search_results["best"]
    abs_best = best["abs"]
    rel_best = best["rel"]

    ### 2. Retrieve results
    best_result = evaluate_custom_alpha(dataset, log_path, abs_best, rel_best)
    default_result = evaluate_custom_alpha(dataset, log_path, abs_threshold=0, rel_threshold=0.0)
    alpha_result = evaluate_pm4py_alpha(dataset, log_path)
    heuristics_result = evaluate_pm4py_heuristics(dataset, log_path)

    ### 3. Visualize best model
    miner = AlphaMinerFrequencies(abs_best, rel_best)
    miner.run(log_path)
    output_file = f"outputs/models/{dataset.replace('.xes', '')}_best_model"
    visualize_model(miner, output_file)

    ### 4. Export YAML results
    export_results_to_yaml(dataset, search_results, best_result, default_result,
                           alpha_result, heuristics_result, miner)

    ### 5. Print Summary if verbose
    if verbose:

        print(f"\n === Evaluation Summary for {dataset} ===")
        print(f"→ Gold standard relations: {len(standards[dataset].direct_succession)}")
        print(f"→ Best config: abs={abs_best}, rel={rel_best:.2f}")
        print("\n--- Best Custom Miner ---")
        print(f"Precision: {best_result['precision']:.3f}")
        print(f"Recall:    {best_result['recall']:.3f}")
        print(f"F1 Score:  {best_result['f1']:.3f}")
        print(f"TP: {best_result['tp']}  FP: {best_result['fp']}  FN: {best_result['fn']}  TN: {best_result['tn']}")

        print("\n--- Default (0, 0) Custom Miner ---")
        print(f"Precision: {default_result['precision']:.3f}")
        print(f"Recall:    {default_result['recall']:.3f}")
        print(f"F1 Score:  {default_result['f1']:.3f}")
        print(f"TP: {default_result['tp']}  FP: {default_result['fp']}  FN: {default_result['fn']}  TN: {default_result['tn']}")

        print("\n--- PM4Py Alpha Miner ---")
        print(f"Precision: {alpha_result['precision']:.3f}")
        print(f"Recall:    {alpha_result['recall']:.3f}")
        print(f"F1 Score:  {alpha_result['f1']:.3f}")
        print(f"TP: {alpha_result['tp']}  FP: {alpha_result['fp']}  FN: {alpha_result['fn']}  TN: {alpha_result['tn']}")

        print("\n--- PM4Py Heuristics Miner ---")
        print(f"Precision: {heuristics_result['precision']:.3f}")
        print(f"Recall:    {heuristics_result['recall']:.3f}")
        print(f"F1 Score:  {heuristics_result['f1']:.3f}")
        print(f"TP: {heuristics_result['tp']}  FP: {heuristics_result['fp']}  FN: {heuristics_result['fn']}  TN: {heuristics_result['tn']}")



if __name__ == "__main__":

    # total 110 param combos
    abs_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] # 10
    rel_values = [0.00, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50] # 11

    # make directories to write to
    os.makedirs("outputs/yamls", exist_ok=True)
    os.makedirs("outputs/models", exist_ok=True)

    # retrieve all dataset names
    datasets = list(standards.keys())

    # Parse the datasets
    for dataset in datasets:
        run_full_analysis_for_dataset(dataset, abs_values, rel_values, verbose=False)

    # Update the html report
    generate_html_from_yaml()

    # Visualize the gold standards
    visualize_all_gold_standards()

    print("\n\nAll datasets processed successfully.")
