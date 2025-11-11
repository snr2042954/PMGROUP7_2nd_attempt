# Alpha Miner with Frequencies – JM0211

**Course:** Process Mining – JM0211  
**Date:** 11/11/2025  

This repository extends the classical *Alpha Miner* algorithm by introducing **frequency-based filtering**.  
It allows process models to be discovered from event logs with configurable **absolute** and **relative frequency thresholds**,  
and evaluates the discovered relations against textbook **gold standard models**.

---

## Overview

### What’s Included
| File / Folder | Description |
|----------------|-------------|
| `utils/gold_standards.py` | Defines textbook Petri net reference models (gold standards). |
| `utils/import_xes.py` | Custom XES parser (simplified alternative to PM4Py’s importer). |
| `alpha_miner.py` | Core implementation of the frequency-based Alpha Miner (hybrid functional + class design). |
| `grid_search.py` | Runs grid search experiments across absolute/relative frequency thresholds. |
| `evaluate.py` | Evaluates PM4Py Alpha Miner, Heuristics Miner, and the custom miner against gold standards. |
| `visualize.py` | Generates Graphviz diagrams for discovered models. |
| `generate_html_from_yaml.py` | Builds an HTML summary report comparing F1-scores across all miners and datasets. |
| `visualize_gold_standards.py` | Generates Graphviz diagrams for gold standard Petri nets. |
| `main.py` | Automates the full pipeline: experiments, YAML export, HTML report, and visualizations. |
| `outputs/` | Contains generated YAML result files, HTML reports, and PNG visualizations. |
| `requirements.txt` | Python dependencies (PM4Py, Graphviz, PyYAML, etc.). |


## Installation

### 1. Clone this repository

```bash
git clone https://github.com/snr2042954/PMGROUP7_2nd_attempt/tree/main
cd PMGROUP7_2nd_attempt
```

### 2. Set up virtual environment

```bash
# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Graphviz

Windows:
Download and install from https://graphviz.org/download/
Then add C:\Program Files\Graphviz\bin to your PATH (logout/login or restart shell).

macOS:
```bash
brew install graphviz
```

### 5. Create and populate data folder

Create a folder named 'data' in root project directory:

```bash
mkdir -p data
```

Fill data folder with all .xes files manually

## Run Experiments

### Run single dataset

```bash
python evaluate.py
```
Runs both PM4Py’s Alpha Miner and the custom frequency-based miner on a single dataset (default: L1.xes).

### Run grid search on one dataset

```bash
python grid_search.py
```

Performs a grid search over combinations of absolute and relative thresholds for one dataset,
printing precision, recall, and F1 for each configuration (default: L1.xes).

Uses a smaller grid for testing purposes:
abs_values = [0,1,2,3]
rel_values = [0.1,0.2,0.3]

### Run all datasets automatically

```bash
python main.py
```

This performs the complete pipeline:

- Runs grid search for each dataset in data/
- Finds the best threshold combination
- Evaluates all miners vs. gold standards
- Exports results as .yaml
- Generates an HTML summary report
- Visualizes both discovered and gold-standard Petri nets

## Results


| Folder	         | Contents                                                         |
|-----------------|------------------------------------------------------------------|
| outputs/yamls/	 | YAML results with metrics, thresholds, and discovered relations. |
|outputs/models/	| Graphviz PNGs for best-performing discovered models.             |
|outputs/gold_standards/	| Visualizations of all gold-standard Petri nets.                  |
|outputs/`comparison_report.html`	| Automatically generated performance comparison dashboard.        |