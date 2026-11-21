# CA2 – Performance Investigation

## Topic
Process Creation vs Thread Creation

## Operating Systems Assignment

This repository contains a Python benchmark comparing process creation and thread creation.

## Experiments

The benchmark examines:

1. Thread and process creation and joining time.
2. CPU-bound workload performance.
3. I/O-bound workload performance.
4. Performance with different numbers of workers.

## Requirements

- Python 3.12 or later

## How to Run

Open PowerShell in the project directory and execute:

```powershell
py src\benchmark.py
```

## Results

The benchmark generates:

`results/benchmark_results.csv`

The CSV contains measurements collected from the computer used to run the experiment.

## Project Structure

- `src/` – Benchmark source code.
- `results/` – Experimental results.
- `report/` – Assignment report.
- `screenshots/` – Screenshots and supporting evidence.

## Note

Results depend on the computer hardware, operating system, and Python version.
