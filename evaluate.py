from pm4py.algo.discovery.alpha import algorithm as alpha_miner
from pm4py.algo.discovery.heuristics import algorithm as heuristics_miner

from alpha_miner import AlphaMinerFrequencies
from utils.gold_standards import standards
from utils.import_xes import read_xes_pm4py


def compute_metrics(discovered: set, gold: set):
    """
    Compute precision, recall, F1-score, and confusion matrix elements:
    TP, FP, FN, TN — based on discovered and gold relations.

    `discovered` and `gold` are sets of (a, b) activity pairs.
    """
    # Derive activity universe from gold and discovered relations
    activities = {a for a, _ in gold | discovered} | {b for _, b in gold | discovered}

    # Generate full set of possible (a, b) activity pairs (excluding self-loops)
    all_possible_pairs = {
        (a, b) for a in activities for b in activities if a != b
    }

    tp_set = discovered & gold
    fp_set = discovered - gold
    fn_set = gold - discovered
    tn_set = all_possible_pairs - (tp_set | fp_set | fn_set)

    tp = len(tp_set)
    fp = len(fp_set)
    fn = len(fn_set)
    tn = len(tn_set)

    precision = tp / (tp + fp) if (tp + fp) else 0
    recall = tp / (tp + fn) if (tp + fn) else 0
    f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) else 0

    return precision, recall, f1, tp, fp, fn, tn


def flatten_pairs(pairs):
    """Convert [['a'], ['b']] pairs into ('a','b') tuples."""
    flat = []
    for pair in pairs:
        a, b = pair
        flat.append((a[0], b[0]))
    return set(flat)


def evaluate_pm4py_alpha(dataset: str, log_path: str):

    gold = standards[dataset]
    gold_relations = gold.direct_succession

    log = read_xes_pm4py(log_path)
    net, initial_marking, final_marking = alpha_miner.apply(log)

    # Extract relations
    relations = set()
    for p in net.places:
        pre = {arc.source.label for arc in p.in_arcs if hasattr(arc.source, "label") and arc.source.label}
        post = {arc.target.label for arc in p.out_arcs if hasattr(arc.target, "label") and arc.target.label}
        for a in pre:
            for b in post:
                relations.add((a, b))

    precision, recall, f1, tp, fp, fn, tn = compute_metrics(relations, gold_relations)

    return {
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "relations": relations,
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "tn": tn
    }


def evaluate_pm4py_heuristics(dataset: str, log_path: str):
    """Run PM4Py Heuristics Miner (default behavior) and return its metrics vs gold standard."""
    gold = standards[dataset]
    gold_relations = gold.direct_succession

    log = read_xes_pm4py(log_path)
    heu_net = heuristics_miner.apply_heu(log)

    # Extract direct succession relations from dependency matrix (without threshold filtering)
    relations = set()
    for src in heu_net.dependency_matrix:
        for tgt in heu_net.dependency_matrix[src]:
            if src != tgt:
                relations.add((src, tgt))

    # Evaluate against gold standard
    precision, recall, f1, tp, fp, fn, tn = compute_metrics(relations, gold_relations)

    return {
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "relations": relations,
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "tn": tn
    }


def evaluate_custom_alpha(dataset: str, log_path: str, abs_threshold: int = 0, rel_threshold: float = 0.0):
    """Run Custom Alpha Miner (frequency-based) and return its metrics vs gold standard."""
    gold = standards[dataset]
    gold_relations = gold.direct_succession

    miner = AlphaMinerFrequencies(abs_threshold=abs_threshold, rel_threshold=rel_threshold)
    miner.run(log_path)
    custom_relations = flatten_pairs(miner.direct_follower)
    precision, recall, f1, tp, fp, fn, tn = compute_metrics(custom_relations, gold_relations)

    return {
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "relations": custom_relations,
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "tn": tn
    }


if __name__ == "__main__":

    ### Configuration ###
    DATASET = "running-example.xes"
    LOG_PATH = f"data/{DATASET}"
    ABS_THRESHOLD = 0
    REL_THRESHOLD = 0.0

    ### Load gold standard ###
    gold = standards[DATASET]
    gold_relations = gold.direct_succession

    print(f"\n=== Evaluating Dataset: {DATASET} ===")
    print(f"Gold Standard ({gold.textbook_figure}): {gold.description}")
    print(f"Gold Standard Relations ({len(gold_relations)}): {gold_relations}\n")

    ### Run evaluations ###
    alpha_results = evaluate_pm4py_alpha(DATASET, LOG_PATH)
    heuristics_results = evaluate_pm4py_heuristics(DATASET, LOG_PATH)
    custom_results = evaluate_custom_alpha(DATASET, LOG_PATH, ABS_THRESHOLD, REL_THRESHOLD)

    ### Print results ###
    print("=== COMPARISON RESULTS ===")
    print(f"Gold Standard Relations: {len(gold_relations)}")
    print(f"PM4Py Alpha Miner Relations: {len(alpha_results['relations'])}")
    print(f"PM4Py Heuristics Miner Relations: {len(heuristics_results['relations'])}")
    print(f"Custom Alpha Miner Relations: {len(custom_results['relations'])}\n")

    print("PM4Py Alpha Miner vs Gold Standard:")
    print(f"  Precision: {alpha_results['precision']:.2f}")
    print(f"  Recall:    {alpha_results['recall']:.2f}")
    print(f"  F1-Score:  {alpha_results['f1']:.2f}")
    print(f"  TP: {alpha_results['tp']}  FP: {alpha_results['fp']}  FN: {alpha_results['fn']}  TN: {alpha_results['tn']}\n")

    print("PM4Py Heuristics Miner vs Gold Standard:")
    print(f"  Precision: {heuristics_results['precision']:.2f}")
    print(f"  Recall:    {heuristics_results['recall']:.2f}")
    print(f"  F1-Score:  {heuristics_results['f1']:.2f}")
    print(f"  TP: {heuristics_results['tp']}  FP: {heuristics_results['fp']}  FN: {heuristics_results['fn']}  TN: {heuristics_results['tn']}\n")

    print("Custom Alpha Miner (Frequencies) vs Gold Standard:")
    print(f"  Precision: {custom_results['precision']:.2f}")
    print(f"  Recall:    {custom_results['recall']:.2f}")
    print(f"  F1-Score:  {custom_results['f1']:.2f}")
    print(f"  TP: {custom_results['tp']}  FP: {custom_results['fp']}  FN: {custom_results['fn']}  TN: {custom_results['tn']}\n")

    print("Done.")
