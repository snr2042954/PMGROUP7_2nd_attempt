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
|----------------|--------------|
| `alpha_miner.py` | Core implementation of the frequency-based Alpha Miner (hybrid: functional + lightweight class). |
| `evaluate.py` | Compares PM4Py’s Alpha Miner and the custom implementation against gold standards. |
| `grid_search.py` | Runs grid search experiments over multiple absolute and relative thresholds. |
| `main.py` | Runs experiments automatically on *all* `.xes` logs found in the `data/` folder. |
| `utils/gold_standards.py` | Contains manually defined textbook reference Petri net structures for all sample logs. |
| `utils/import_xes.py` | Lightweight XES parser used by the custom miner. |
| `requirements.txt` | All dependencies needed for running experiments (PM4Py, matplotlib, etc.). |
| `results.txt` | Example experiment output (console logs). |

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
printing precision, recall, and F1 for each configuration.

### Run all datasets automatically

```bash
python main.py
```

This script:

- Scans the data/ folder for all .xes files.
- Runs the grid search experiment on each.
- Prints a summary of the best F1 score per dataset.