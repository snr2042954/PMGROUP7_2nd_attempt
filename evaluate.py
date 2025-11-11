from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.algo.discovery.alpha import algorithm as alpha_miner
from pm4py.algo.discovery.dfg import algorithm as dfg_factory

from alpha_miner import AlphaMinerFrequencies
from utils.gold_standards import standards

# ---------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------

def compute_metrics(discovered: set, gold: set):
    intersection = discovered & gold
    precision = len(intersection) / len(discovered) if discovered else 0
    recall = len(intersection) / len(gold) if gold else 0
    f1 = (
        2 * precision * recall / (precision + recall)
        if (precision + recall) > 0
        else 0
    )
    return precision, recall, f1, intersection


def flatten_pairs(pairs):
    """Convert [['a'], ['b']] pairs into ('a','b') tuples."""
    flat = []
    for pair in pairs:
        a, b = pair
        flat.append((a[0], b[0]))
    return set(flat)

def evaluate_pm4py_alpha(dataset: str, log_path: str):
    """Run PM4Py Alpha Miner and return its metrics vs gold standard."""
    gold = standards[dataset]
    gold_relations = gold.direct_succession

    log = xes_importer.apply(log_path)
    dfg = dfg_factory.apply(log)
    relations = set((a, b) for (a, b), freq in dfg.items() if a != b)
    precision, recall, f1, _ = compute_metrics(relations, gold_relations)

    return {
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "relations": relations,
    }


def evaluate_custom_alpha(dataset: str, log_path: str, abs_threshold: int = 0, rel_threshold: float = 0.0):
    """Run Custom Alpha Miner with thresholds and return its metrics vs gold standard."""
    gold = standards[dataset]
    gold_relations = gold.direct_succession

    miner = AlphaMinerFrequencies(abs_threshold=abs_threshold, rel_threshold=rel_threshold)
    miner.run(log_path)
    custom_relations = flatten_pairs(miner.direct_follower)
    precision, recall, f1, _ = compute_metrics(custom_relations, gold_relations)

    return {
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "relations": custom_relations,
    }


if __name__ == "__main__":

    ### Configuration ###
    DATASET = "L1.xes"
    LOG_PATH = f"data/{DATASET}"
    ABS_THRESHOLD = 0
    REL_THRESHOLD = 0.0

    ### Load gold standard ###
    gold = standards[DATASET]
    gold_relations = gold.direct_succession

    print(f"\n=== Evaluating Dataset: {DATASET} ===")
    print(f"Gold Standard ({gold.textbook_figure}): {gold.description}")
    print(f"Gold Standard Relations ({len(gold_relations)}): {gold_relations}\n")

    ### Run both evaluations ###
    pm4py_results = evaluate_pm4py_alpha(DATASET, LOG_PATH)
    custom_results = evaluate_custom_alpha(DATASET, LOG_PATH, ABS_THRESHOLD, REL_THRESHOLD)

    ### Print results ###
    print("=== COMPARISON RESULTS ===")
    print(f"Gold Standard Relations: {len(gold_relations)}")
    print(f"PM4Py Alpha Miner Relations: {len(pm4py_results['relations'])}")
    print(f"Custom Alpha Miner Relations: {len(custom_results['relations'])}\n")

    print("PM4Py vs Gold Standard:")
    print(f"  Precision: {pm4py_results['precision']:.2f}")
    print(f"  Recall:    {pm4py_results['recall']:.2f}")
    print(f"  F1-Score:  {pm4py_results['f1']:.2f}\n")

    print("Custom Alpha Miner vs Gold Standard:")
    print(f"  Precision: {custom_results['precision']:.2f}")
    print(f"  Recall:    {custom_results['recall']:.2f}")
    print(f"  F1-Score:  {custom_results['f1']:.2f}\n")

    print("Done.")
