# Alpha Miner with Frequencies – JM0211

**Course:** Process Mining – JM0211  
**Date:** 11/11/2025  

This repository extends the classical *Alpha Miner* algorithm by introducing **frequency-based filtering**.  
It allows process models to be discovered from event logs with configurable **absolute** and **relative frequency thresholds**,  
and evaluates the discovered relations against textbook **gold standard models**.

---

## Overview

### What's Included
| File / Folder | Description |
|----------------|--------------|
| `alpha_miner.py` | Core implementation of the frequency-based Alpha Miner (hybrid: functional + lightweight class). |
| `evaluate.py` | Compares PM4Py's Alpha Miner, PM4Py's Heuristics Miner, and the custom implementation against gold standards. Includes confusion matrix metrics (TP, FP, FN, TN). |
| `grid_search.py` | Runs grid search experiments over multiple absolute and relative thresholds. |
| `main.py` | Runs experiments automatically on *all* `.xes` logs found in the `data/` folder. Generates visualizations and evaluation summaries. |
| `generate_report.py` | Generates HTML comparison reports from `results.txt` with detailed metrics and confusion matrices. |
| `visualize.py` | Visualizes discovered Petri net models using Graphviz. |
| `visualize_gold_standards.py` | Visualizes gold standard Petri net models using PM4Py. |
| `utils/gold_standards.py` | Contains manually defined textbook reference Petri net structures for all sample logs. |
| `utils/import_xes.py` | Lightweight XES parser used by the custom miner, with PM4Py compatibility helpers. |
| `requirements.txt` | All dependencies needed for running experiments (PM4Py, matplotlib, graphviz, pyyaml, etc.). |
| `results.txt` | Experiment output (console logs) with evaluation metrics. |
| `results/comparison_report.html` | HTML report comparing all miners across datasets. |

## Installation

### 1. Set up virtual environment

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create and populate data folder

Create a folder named 'data' in root project directory. Fill with all .xes files

## Run Experiments

### Run single dataset evaluation

```bash
python evaluate.py
```
Runs PM4Py's Alpha Miner, PM4Py's Heuristics Miner, and the custom frequency-based miner on a single dataset (default: running-example.xes). Outputs precision, recall, F1, and confusion matrix metrics (TP, FP, FN, TN).

### Run grid search on one dataset

```bash
python grid_search.py
```

Performs a grid search over combinations of absolute and relative thresholds for one dataset,
printing precision, recall, and F1 for each configuration.

### Run all dataset evaluations automatically

```bash
python main.py
```

or to automatically save output to `results.txt`:

```bash
python main.py --save
```

This script:

- Runs grid search experiments on all datasets in the `data/` folder.
- Evaluates best custom miner, default custom miner, PM4Py Alpha Miner, and PM4Py Heuristics Miner.
- Prints comprehensive evaluation summaries with confusion matrix metrics.
- Generates visualizations of the best discovered models (saved to `outputs/`).

### Generate HTML comparison report

```bash
python generate_report.py
```

Generates an HTML report (`results/comparison_report.html`) comparing:
- PM4Py Alpha Miner vs Default Custom Miner
- PM4Py Alpha Miner vs Best Custom Miner (from grid search)
- PM4Py Heuristics Miner vs Best Custom Miner

The report includes precision, recall, F1 scores, confusion matrices (TP/FP/FN/TN), and F1 difference metrics.

### Visualize gold standard models

```bash
# Visualize all gold standards
python visualize_gold_standards.py

# Visualize a specific dataset
python visualize_gold_standards.py L1.xes
```

Generates PM4Py visualizations of the gold standard Petri nets (saved to `results/gold_standard_visualizations/`).