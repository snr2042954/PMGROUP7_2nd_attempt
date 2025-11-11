"""Generate HTML report comparing different miners across datasets."""

import os
import re


def parse_results_txt(results_file="results.txt"):
    """Parse results.txt to extract evaluation data."""
    with open(results_file, 'r') as f:
        content = f.read()
    
    datasets = []
    current_dataset = None
    
    # Pattern to match dataset sections
    dataset_pattern = r"Dataset: (.+\.xes)"
    summary_pattern = r"📊 === Evaluation Summary for (.+\.xes) ==="
    best_config_pattern = r"→ Best config: abs=(\d+), rel=([\d.]+)"
    
    # Patterns for metrics (with optional confusion matrix)
    pm4py_alpha_pattern = r"--- PM4Py Alpha Miner ---\s+Precision: ([\d.]+)\s+Recall:\s+([\d.]+)\s+F1 Score:\s+([\d.]+)(?:\s+TP: (\d+), FP: (\d+), FN: (\d+), TN: (\d+))?"
    pm4py_heuristics_pattern = r"--- PM4Py Heuristics Miner ---\s+Precision: ([\d.]+)\s+Recall:\s+([\d.]+)\s+F1 Score:\s+([\d.]+)(?:\s+TP: (\d+), FP: (\d+), FN: (\d+), TN: (\d+))?"
    default_custom_pattern = r"--- Default \(0, 0\) Custom Miner ---\s+Precision: ([\d.]+)\s+Recall:\s+([\d.]+)\s+F1 Score:\s+([\d.]+)(?:\s+TP: (\d+), FP: (\d+), FN: (\d+), TN: (\d+))?"
    best_custom_pattern = r"--- Best Custom Miner ---\s+Precision: ([\d.]+)\s+Recall:\s+([\d.]+)\s+F1 Score:\s+([\d.]+)(?:\s+TP: (\d+), FP: (\d+), FN: (\d+), TN: (\d+))?"
    
    # Split by dataset sections
    sections = re.split(r"============================\s+Dataset: (.+\.xes)", content)
    
    for i in range(1, len(sections), 2):
        if i + 1 < len(sections):
            dataset = sections[i]
            section_content = sections[i + 1]
            
            # Extract best config
            best_match = re.search(best_config_pattern, section_content)
            best_abs = int(best_match.group(1)) if best_match else 1
            best_rel = float(best_match.group(2)) if best_match else 0.0
            
            # Extract metrics
            pm4py_alpha_match = re.search(pm4py_alpha_pattern, section_content)
            pm4py_heuristics_match = re.search(pm4py_heuristics_pattern, section_content)
            default_custom_match = re.search(default_custom_pattern, section_content)
            best_custom_match = re.search(best_custom_pattern, section_content)
            
            if all([pm4py_alpha_match, pm4py_heuristics_match, default_custom_match, best_custom_match]):
                def extract_metrics(match):
                    """Extract metrics from regex match, handling optional confusion matrix."""
                    metrics = {
                        "precision": float(match.group(1)),
                        "recall": float(match.group(2)),
                        "f1": float(match.group(3))
                    }
                    # Optional confusion matrix (groups 4-7)
                    if match.group(4) is not None:
                        metrics["tp"] = int(match.group(4))
                        metrics["fp"] = int(match.group(5))
                        metrics["fn"] = int(match.group(6))
                        metrics["tn"] = int(match.group(7))
                    else:
                        metrics["tp"] = None
                        metrics["fp"] = None
                        metrics["fn"] = None
                        metrics["tn"] = None
                    return metrics
                
                datasets.append({
                    "dataset": dataset,
                    "best_abs": best_abs,
                    "best_rel": best_rel,
                    "pm4py_alpha": extract_metrics(pm4py_alpha_match),
                    "pm4py_heuristics": extract_metrics(pm4py_heuristics_match),
                    "default_custom": extract_metrics(default_custom_match),
                    "best_custom": extract_metrics(best_custom_match)
                })
    
    return datasets


def generate_html_report(output_file="results/comparison_report.html", results_file="results.txt"):
    """Generate HTML report with 3 comparison tables from results.txt."""
    
    os.makedirs("results", exist_ok=True)
    
    print("Parsing results.txt...")
    datasets = parse_results_txt(results_file)
    print(f"Found {len(datasets)} datasets")
    
    # Organize data for tables
    table1_data = []  # PM4Py Alpha vs Default Custom
    table2_data = []  # PM4Py Alpha vs Best Custom
    table3_data = []  # PM4Py Heuristics vs Best Custom
    
    for data in datasets:
        table1_data.append({
            "dataset": data["dataset"],
            "pm4py_alpha": data["pm4py_alpha"],
            "default_custom": data["default_custom"]
        })
        
        table2_data.append({
            "dataset": data["dataset"],
            "pm4py_alpha": data["pm4py_alpha"],
            "best_custom": data["best_custom"],
            "best_params": {"abs": data["best_abs"], "rel": data["best_rel"]}
        })
        
        table3_data.append({
            "dataset": data["dataset"],
            "pm4py_heuristics": data["pm4py_heuristics"],
            "best_custom": data["best_custom"],
            "best_params": {"abs": data["best_abs"], "rel": data["best_rel"]}
        })
    
    # Generate HTML
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Alpha Miner Comparison Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        h1 {{
            color: #333;
            text-align: center;
        }}
        h2 {{
            color: #555;
            margin-top: 40px;
            border-bottom: 2px solid #333;
            padding-bottom: 10px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background-color: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        th {{
            background-color: #4CAF50;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: bold;
        }}
        td {{
            padding: 10px;
            border-bottom: 1px solid #ddd;
        }}
        tr:hover {{
            background-color: #f5f5f5;
        }}
        .dataset {{
            font-weight: bold;
            color: #333;
        }}
        .metric {{
            text-align: right;
        }}
        .f1-high {{
            color: #2e7d32;
            font-weight: bold;
        }}
        .f1-medium {{
            color: #f57c00;
        }}
        .f1-low {{
            color: #c62828;
        }}
        .diff-positive {{
            color: #2e7d32;
            font-weight: bold;
        }}
        .diff-negative {{
            color: #c62828;
            font-weight: bold;
        }}
        .diff-zero {{
            color: #666;
        }}
    </style>
</head>
<body>
    <h1>Alpha Miner Comparison Report</h1>
    <p style="text-align: center; color: #666;">Generated comparison of PM4Py and Custom Alpha Miner implementations</p>
    
    <h2>Table 1: PM4Py Alpha Miner vs Default Custom Miner (abs=1, rel=0.0)</h2>
    <table>
        <thead>
            <tr>
                <th>Dataset</th>
                <th>PM4Py Alpha - Precision</th>
                <th>PM4Py Alpha - Recall</th>
                <th>PM4Py Alpha - F1</th>
                <th>PM4Py Alpha - TP/FP/FN/TN</th>
                <th>Default Custom - Precision</th>
                <th>Default Custom - Recall</th>
                <th>Default Custom - F1</th>
                <th>Default Custom - TP/FP/FN/TN</th>
                <th>F1 Difference (Custom - PM4Py)</th>
            </tr>
        </thead>
        <tbody>
"""
    
    for row in table1_data:
        pa = row["pm4py_alpha"]
        dc = row["default_custom"]
        f1_diff = dc['f1'] - pa['f1']
        diff_class = 'diff-positive' if f1_diff > 0 else 'diff-negative' if f1_diff < 0 else 'diff-zero'
        diff_sign = '+' if f1_diff > 0 else ''
        
        # Format confusion matrix
        pa_cm = f"{pa['tp']}/{pa['fp']}/{pa['fn']}/{pa['tn']}" if pa['tp'] is not None else "N/A"
        dc_cm = f"{dc['tp']}/{dc['fp']}/{dc['fn']}/{dc['tn']}" if dc['tp'] is not None else "N/A"
        
        html += f"""            <tr>
                <td class="dataset">{row['dataset']}</td>
                <td class="metric">{pa['precision']:.3f}</td>
                <td class="metric">{pa['recall']:.3f}</td>
                <td class="metric f1-{'high' if pa['f1'] >= 0.8 else 'medium' if pa['f1'] >= 0.5 else 'low'}">{pa['f1']:.3f}</td>
                <td class="metric">{pa_cm}</td>
                <td class="metric">{dc['precision']:.3f}</td>
                <td class="metric">{dc['recall']:.3f}</td>
                <td class="metric f1-{'high' if dc['f1'] >= 0.8 else 'medium' if dc['f1'] >= 0.5 else 'low'}">{dc['f1']:.3f}</td>
                <td class="metric">{dc_cm}</td>
                <td class="metric {diff_class}">{diff_sign}{f1_diff:.3f}</td>
            </tr>
"""
    
    html += """        </tbody>
    </table>
    
    <h2>Table 2: PM4Py Alpha Miner vs Best Custom Miner (from Grid Search)</h2>
    <table>
        <thead>
            <tr>
                <th>Dataset</th>
                <th>Best Params (abs, rel)</th>
                <th>PM4Py Alpha - Precision</th>
                <th>PM4Py Alpha - Recall</th>
                <th>PM4Py Alpha - F1</th>
                <th>PM4Py Alpha - TP/FP/FN/TN</th>
                <th>Best Custom - Precision</th>
                <th>Best Custom - Recall</th>
                <th>Best Custom - F1</th>
                <th>Best Custom - TP/FP/FN/TN</th>
                <th>F1 Difference (Custom - PM4Py)</th>
            </tr>
        </thead>
        <tbody>
"""
    
    for row in table2_data:
        pa = row["pm4py_alpha"]
        bc = row["best_custom"]
        params = row["best_params"]
        f1_diff = bc['f1'] - pa['f1']
        diff_class = 'diff-positive' if f1_diff > 0 else 'diff-negative' if f1_diff < 0 else 'diff-zero'
        diff_sign = '+' if f1_diff > 0 else ''
        
        # Format confusion matrix
        pa_cm = f"{pa['tp']}/{pa['fp']}/{pa['fn']}/{pa['tn']}" if pa['tp'] is not None else "N/A"
        bc_cm = f"{bc['tp']}/{bc['fp']}/{bc['fn']}/{bc['tn']}" if bc['tp'] is not None else "N/A"
        
        html += f"""            <tr>
                <td class="dataset">{row['dataset']}</td>
                <td>({params['abs']}, {params['rel']:.2f})</td>
                <td class="metric">{pa['precision']:.3f}</td>
                <td class="metric">{pa['recall']:.3f}</td>
                <td class="metric f1-{'high' if pa['f1'] >= 0.8 else 'medium' if pa['f1'] >= 0.5 else 'low'}">{pa['f1']:.3f}</td>
                <td class="metric">{pa_cm}</td>
                <td class="metric">{bc['precision']:.3f}</td>
                <td class="metric">{bc['recall']:.3f}</td>
                <td class="metric f1-{'high' if bc['f1'] >= 0.8 else 'medium' if bc['f1'] >= 0.5 else 'low'}">{bc['f1']:.3f}</td>
                <td class="metric">{bc_cm}</td>
                <td class="metric {diff_class}">{diff_sign}{f1_diff:.3f}</td>
            </tr>
"""
    
    html += """        </tbody>
    </table>
    
    <h2>Table 3: PM4Py Heuristics Miner vs Best Custom Miner (from Grid Search)</h2>
    <table>
        <thead>
            <tr>
                <th>Dataset</th>
                <th>Best Params (abs, rel)</th>
                <th>PM4Py Heuristics - Precision</th>
                <th>PM4Py Heuristics - Recall</th>
                <th>PM4Py Heuristics - F1</th>
                <th>PM4Py Heuristics - TP/FP/FN/TN</th>
                <th>Best Custom - Precision</th>
                <th>Best Custom - Recall</th>
                <th>Best Custom - F1</th>
                <th>Best Custom - TP/FP/FN/TN</th>
                <th>F1 Difference (Custom - PM4Py)</th>
            </tr>
        </thead>
        <tbody>
"""
    
    for row in table3_data:
        ph = row["pm4py_heuristics"]
        bc = row["best_custom"]
        params = row["best_params"]
        f1_diff = bc['f1'] - ph['f1']
        diff_class = 'diff-positive' if f1_diff > 0 else 'diff-negative' if f1_diff < 0 else 'diff-zero'
        diff_sign = '+' if f1_diff > 0 else ''
        
        # Format confusion matrix
        ph_cm = f"{ph['tp']}/{ph['fp']}/{ph['fn']}/{ph['tn']}" if ph['tp'] is not None else "N/A"
        bc_cm = f"{bc['tp']}/{bc['fp']}/{bc['fn']}/{bc['tn']}" if bc['tp'] is not None else "N/A"
        
        html += f"""            <tr>
                <td class="dataset">{row['dataset']}</td>
                <td>({params['abs']}, {params['rel']:.2f})</td>
                <td class="metric">{ph['precision']:.3f}</td>
                <td class="metric">{ph['recall']:.3f}</td>
                <td class="metric f1-{'high' if ph['f1'] >= 0.8 else 'medium' if ph['f1'] >= 0.5 else 'low'}">{ph['f1']:.3f}</td>
                <td class="metric">{ph_cm}</td>
                <td class="metric">{bc['precision']:.3f}</td>
                <td class="metric">{bc['recall']:.3f}</td>
                <td class="metric f1-{'high' if bc['f1'] >= 0.8 else 'medium' if bc['f1'] >= 0.5 else 'low'}">{bc['f1']:.3f}</td>
                <td class="metric">{bc_cm}</td>
                <td class="metric {diff_class}">{diff_sign}{f1_diff:.3f}</td>
            </tr>
"""
    
    html += """        </tbody>
    </table>
    
    <footer style="margin-top: 40px; text-align: center; color: #666; font-size: 0.9em;">
        <p>Report generated automatically from evaluation results</p>
    </footer>
</body>
</html>"""
    
    with open(output_file, 'w') as f:
        f.write(html)
    
    print(f"\n✓ HTML report generated: {output_file}")
    return output_file


if __name__ == "__main__":
    generate_html_report()

