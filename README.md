# DevOps Exercise

[![Python application](https://github.com/norus04/capstone-hw5/actions/workflows/main.yml/badge.svg)](https://github.com/norus04/capstone-hw5/actions/workflows/main.yml)

This repository implements three sorting algorithms and a basic DevOps workflow using pre-commit hooks, linting, automated testing, and multi-platform CI/CD.

## Implemented Algorithms
Each sorting algorithm is wrapped with a performance-tracking helper. All algorithms return a new sorted list and leave the original list as is.

**Bubble Sort**
It repeatedly goes through the list and swaps neighboring values that are out of order.

**Quicksort**
A recursive approach that picks a pivot, looks at the data around it, and sorts the sublists.

**Insertion Sort**
Builds up the sorted list one element at a time by inserting each new value into its correct position.

## Performance
Each algorithm has a measurement wrapper:
- Collects average CPU time
- Collects memory usage (via RSS bytes)

## DevOps Workflow
This repository follows a small DevOps workflow to ensure code quality and reproducibility across various OS's.

### Pre-Commit Hooks
The `.pre-commit-config.yaml` file has many checks before a commit is allowed:
- Prevents committing very large files  
- Runs Black for code formatting  
- Runs flake8 for style enforcement  
- Scans for accidentally committed private keys

### **Linting**
- Black automatically formats all Python files to a standard style.  
- flake* checks for unused imports, style violations, and common errors.

Both tools run locally.

### Tests
All tests are written with pytest. These tests do the following:
- Verify correctness of the three sorting algorithms
- Print out performance statistics

Running the tests shows log lines like:
[MEASURE] bubble avg_cpu_time=1.882335s avg_rss_bytes=26214

### CI Measurement Table

Dataset size: n = 5000 integers, averaged over 5 runs per OS.

| OS       | Python | Bubble avg_cpu_time (s) | Quick avg_cpu_time (s) | Insertion avg_rss_bytes | Insertion after_rss_bytes |
|----------|---------|--------------------------|--------------------------|-------------------------------|--------------------------------|
| Windows  | 3.9     | 1.393625                 | 0.004478                 | 74547                         | 43225088                       |
| Windows  | 3.10    | 1.441940                 | 0.004725                 | 0                             | 43761664                       |
| Ubuntu   | 3.9     | 1.882335                 | 0.004490                 | 0                             | 48197632                       |
| Ubuntu   | 3.10    | 1.504698                 | 0.003887                 | 0                             | 48828416                       |
| macOS    | 3.9     | 1.511124                 | 0.003791                 | 0                             | 41648128                       |
| macOS    | 3.10    | 1.114731                 | 0.002569                 | 19661                         | 42827776                       |

**Notes:**
- `avg_rss_bytes` is the average RSS change per run. Some OSes report 0 when memory change is too small or stabilized by the runtime.
- `after_rss_bytes` is the RSS of the Python process after insertion sort completes.


## How to Run
Install dependencies:
make install

Run tests:
make tests

Local lint check:
make lint

