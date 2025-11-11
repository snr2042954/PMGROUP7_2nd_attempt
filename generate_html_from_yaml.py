"""
Generate HTML report:
1️⃣ Best Custom Miner results (detailed metrics)
2️⃣ Comparison of all miners (F1-scores)
"""

import os
import yaml

# --- loader fix for !!python/tuple tags ---
class TupleSafeLoader(yaml.SafeLoader):
    pass
def construct_python_tuple(loader, node):
    return tuple(loader.construct_sequence(node))
TupleSafeLoader.add_constructor(u'tag:yaml.org,2002:python/tuple', construct_python_tuple)


def load_yaml_results(folder="outputs/yamls"):
    """Load YAML result files from the given folder."""
    datasets = []
    for file in sorted(os.listdir(folder)):
        if not file.endswith(".yaml"):
            continue
        with open(os.path.join(folder, file), "r") as f:
            data = yaml.load(f, Loader=TupleSafeLoader)

        dataset = data["dataset"]
        params = data.get("best_parameters", {})

        def get_eval(key):
            sec = data.get(key, {})
            return {
                "precision": sec.get("precision", 0.0),
                "recall": sec.get("recall", 0.0),
                "f1": sec.get("f1", 0.0),
                "tp": sec.get("tp"),
                "fp": sec.get("fp"),
                "fn": sec.get("fn"),
                "tn": sec.get("tn"),
            }

        datasets.append({
            "dataset": dataset,
            "params": (params.get("abs_threshold", 0), params.get("rel_threshold", 0.0)),
            "custom_best": get_eval("evaluation_custom"),
            "custom_default": get_eval("evaluation_default"),
            "alpha": get_eval("evaluation_alpha"),
            "heuristic": get_eval("evaluation_heuristic"),
        })
    return datasets


def f1_class(value: float) -> str:
    """Return CSS class based on F1 value."""
    if value >= 0.8:
        return "f1-high"
    elif value >= 0.5:
        return "f1-medium"
    else:
        return "f1-low"


def generate_html_from_yaml(output_file="outputs/comparison_report.html", folder="outputs/yamls"):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    datasets = load_yaml_results(folder)

    # --- HTML HEADER ---
    html = """<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Alpha Miner Comparison Report</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 25px; background: #f7f7f7; }
    h1, h2 { color: #333; text-align: center; }
    table { width: 100%; border-collapse: collapse; margin: 25px 0; background: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    th { background: #4CAF50; color: white; padding: 10px; text-align: center; }
    td { padding: 8px; text-align: center; border-bottom: 1px solid #ddd; }
    tr:hover { background-color: #f5f5f5; }
    .dataset { text-align: left; font-weight: bold; }
    .f1-high { color: #2e7d32; font-weight: bold; }
    .f1-medium { color: #f57c00; font-weight: bold; }
    .f1-low { color: #c62828; font-weight: bold; }
  </style>
</head>
<body>
  <h1>Alpha Miner Comparison Report</h1>
"""

    # --- TABLE 1: Best Custom Miner Detailed Results ---
    html += """
  <h2>Summary of Best Custom Miner Results (from Grid Search)</h2>
  <table>
    <thead>
      <tr>
        <th>Dataset</th>
        <th>Best Params (abs, rel)</th>
        <th>Precision</th>
        <th>Recall</th>
        <th>F1 Score</th>
        <th>TP</th>
        <th>FP</th>
        <th>FN</th>
        <th>TN</th>
      </tr>
    </thead>
    <tbody>
"""

    for d in datasets:
        cb = d["custom_best"]
        html += f"""      <tr>
        <td class="dataset">{d['dataset']}</td>
        <td>({d['params'][0]}, {d['params'][1]:.2f})</td>
        <td>{cb['precision']:.3f}</td>
        <td>{cb['recall']:.3f}</td>
        <td class="{f1_class(cb['f1'])}">{cb['f1']:.3f}</td>
        <td>{cb['tp'] if cb['tp'] is not None else '–'}</td>
        <td>{cb['fp'] if cb['fp'] is not None else '–'}</td>
        <td>{cb['fn'] if cb['fn'] is not None else '–'}</td>
        <td>{cb['tn'] if cb['tn'] is not None else '–'}</td>
      </tr>
"""

    html += """    </tbody>
  </table>
"""

    # --- TABLE 2: Comparison of All Methods ---
    html += """
  <h2>Comparison of F1 Scores Across All Methods</h2>
  <table>
    <thead>
      <tr>
        <th>Dataset</th>
        <th>Best Params (abs, rel)</th>
        <th>Custom (0,0)</th>
        <th>Custom (Best)</th>
        <th>PM4Py Alpha</th>
        <th>PM4Py Heuristic</th>
      </tr>
    </thead>
    <tbody>
"""

    for d in datasets:
        cd, cb, al, he = d["custom_default"], d["custom_best"], d["alpha"], d["heuristic"]
        html += f"""      <tr>
        <td class="dataset">{d['dataset']}</td>
        <td>({d['params'][0]}, {d['params'][1]:.2f})</td>
        <td class="{f1_class(cd['f1'])}">{cd['f1']:.3f}</td>
        <td class="{f1_class(cb['f1'])}">{cb['f1']:.3f}</td>
        <td class="{f1_class(al['f1'])}">{al['f1']:.3f}</td>
        <td class="{f1_class(he['f1'])}">{he['f1']:.3f}</td>
      </tr>
"""

    html += """    </tbody>
  </table>

  <footer style="text-align:center;color:#666;margin-top:30px;font-size:0.9em;">
    Report generated automatically from YAML exports.
  </footer>
</body>
</html>
"""

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"HTML report generated: {output_file}")
    return output_file


if __name__ == "__main__":
    generate_html_from_yaml()
