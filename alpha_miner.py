"""
Alpha Miner with Frequencies (hybrid version)
---------------------------------------------

- Functional core: each step has one clear purpose
- Lightweight coordinating class: wraps configuration + results
- Compatible with existing evaluation code (exposes .direct_follower etc.)

Author: Bram Donkers
Date: 11/11/2025
"""

from utils.import_xes import read_xes
from collections import defaultdict


def compute_direct_followers(traces):
    """Compute direct followers and their frequencies."""
    df_counts = defaultdict(int)
    total_out = defaultdict(int)

    for trace in traces:
        for i in range(len(trace) - 1):
            a, b = trace[i], trace[i + 1]
            df_counts[(a, b)] += 1
            total_out[a] += 1

    freq = []
    for (a, b), abs_f in df_counts.items():
        rel_f = abs_f / total_out[a]
        freq.append({"pair": ([a], [b]), "abs_freq": abs_f, "rel_freq": rel_f})

    return freq


def filter_by_frequency(freq_data, abs_threshold, rel_threshold):
    """Keep pairs above absolute and relative thresholds."""
    return [
        item["pair"]
        for item in freq_data
        if item["abs_freq"] >= abs_threshold and item["rel_freq"] >= rel_threshold
    ]


def detect_parallel_and_causality(direct_followers):
    """Separate parallel and causal relations."""
    parallel = []
    causality = list(direct_followers)

    for i in range(len(direct_followers)):
        for j in range(i + 1, len(direct_followers)):
            a1, b1 = direct_followers[i]
            a2, b2 = direct_followers[j]
            if a1 == b2 and b1 == a2 and (a1 != b1):
                parallel.append(direct_followers[i])
                if direct_followers[i] in causality:
                    causality.remove(direct_followers[i])
                if direct_followers[j] in causality:
                    causality.remove(direct_followers[j])
    return parallel, causality


def compute_Xw_Yw(causality, parallel):
    """Compute X_w and Y_w sets."""
    X_w = list(causality)
    Y_w = list(X_w)
    merged = []

    for fb in range(2):
        for i in range(len(X_w)):
            temp = []
            for j in range(i, len(X_w)):
                if X_w[i][fb] == X_w[j][fb]:
                    temp.append(X_w[j][1 - fb])
            if len(temp) > 1 and temp not in parallel:
                single = sum(temp, [])
                if fb == 0:
                    merged.append([X_w[i][fb], single])
                else:
                    merged.append([single, X_w[i][fb]])

    X_w += merged
    Y_w += merged
    return X_w, Y_w


def compute_places(Y_w):
    """Generate place set P_w."""
    return ["I_w"] + [f"P{i}" for i in range(len(Y_w))] + ["O_w"]


def compute_flows(Y_w, P_w, T_i, T_o):
    """Generate flow relation F_w."""
    F_w = [[P_w[0], T_i]]
    for idx, y in enumerate(Y_w, start=1):
        for i in y[0]:
            F_w.append([i, P_w[idx]])
        for i in y[1]:
            F_w.append([P_w[idx], i])
    F_w.append([T_o, P_w[-1]])
    return F_w

class AlphaMinerFrequencies:
    """Coordinates frequency-based Alpha Miner execution."""

    def __init__(self, abs_threshold=1, rel_threshold=0.0):
        self.abs_threshold = abs_threshold
        self.rel_threshold = rel_threshold

        # Results (for evaluate.py compatibility)
        self.direct_follower = []
        self.direct_follower_freq = []
        self.parallel = []
        self.causality = []
        self.X_w = []
        self.Y_w = []
        self.P_w = []
        self.F_w = []
        self.T_i = None
        self.T_o = None
        self.T_w = []

    def run(self, path):
        """Run Alpha Miner end-to-end on a log path."""
        log_dict = read_xes(path)
        traces = list(log_dict.values())
        if not traces:
            print("No traces found.")
            return None

        self.T_w = sorted({a for t in traces for a in t})
        self.T_i, self.T_o = traces[0][0], traces[0][-1]

        # Step 1: direct followers
        self.direct_follower_freq = compute_direct_followers(traces)
        self.direct_follower = filter_by_frequency(
            self.direct_follower_freq, self.abs_threshold, self.rel_threshold
        )

        # Step 2: relations
        self.parallel, self.causality = detect_parallel_and_causality(
            self.direct_follower
        )

        # Step 3: model components
        self.X_w, self.Y_w = compute_Xw_Yw(self.causality, self.parallel)
        self.P_w = compute_places(self.Y_w)
        self.F_w = compute_flows(self.Y_w, self.P_w, self.T_i, self.T_o)

        return {
            "direct_follower": self.direct_follower,
            "causality": self.causality,
            "parallel": self.parallel,
            "P_w": self.P_w,
            "F_w": self.F_w,
        }


# -----------------------------------------------------------------------------
# Example usage
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    miner = AlphaMinerFrequencies(abs_threshold=0, rel_threshold=0)
    miner.run("data/L1.xes")

    print("\nDirect followers:", miner.direct_follower)
    print("Causality:", miner.causality)
    print("Parallel:", miner.parallel)
    print("Places:", miner.P_w)
    print("Flows:", miner.F_w)
