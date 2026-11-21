# CA2 – Performance Investigation

## Process Creation vs Thread Creation

**Course:** Operating Systems  
**Assignment:** CA2 – Performance Investigation  
**Language:** Python 3

## 1. Project Overview

This project investigates the performance differences between creating processes and creating threads in Python.

It compares their creation overhead and execution performance under CPU-bound and I/O-bound workloads.

## 2. Objectives

- Measure thread creation and joining time.
- Measure process creation and joining time.
- Compare thread and process execution for CPU-bound tasks.
- Compare thread and process execution for I/O-bound tasks.
- Observe how performance changes with different worker counts.

## 3. Technologies Used

- Python 3.14.0
- Python `threading` and `multiprocessing` libraries
- `concurrent.futures`
- CSV for storing benchmark results
- Git and GitHub for version control

## 4. Project Structure

```text
Performance-Investigation/
├── src/
│   └── benchmark.py
├── results/
│   └── benchmark_results.csv
├── report/
├── screenshots/
├── README.md
├── requirements.txt
└── .gitignore
```

## 5. How to Run

Make sure Python is installed.

Open PowerShell in the project directory and execute:

```powershell
py src\benchmark.py
```

The program runs the benchmarks and saves the measurements to:

`results/benchmark_results.csv`

## 6. Experimental Results

The following measurements were collected on the computer used for this experiment.

**Environment:** Python 3.14.0, 20 CPU cores.

### A. Creation and Joining Time

| Type | Time |
|---|---:|
| Thread | 552.93 µs |
| Process | 142312.03 µs |

### B. CPU-bound Workload

| Execution type | Workers | Time |
|---|---:|---:|
| Thread | 1 | 148.666 ms |
| Thread | 2 | 143.844 ms |
| Thread | 4 | 143.504 ms |
| Process | 1 | 300.533 ms |
| Process | 2 | 246.504 ms |
| Process | 4 | 256.648 ms |

### C. I/O-bound Workload

| Execution type | Workers | Time |
|---|---:|---:|
| Thread | 1 | 406.471 ms |
| Thread | 2 | 206.094 ms |
| Thread | 4 | 103.662 ms |
| Process | 1 | 567.465 ms |
| Process | 2 | 375.357 ms |
| Process | 4 | 318.673 ms |

## 7. Observations

- Thread creation and joining took less time than process creation and joining in this experiment.
- Threads performed faster than processes in the tested CPU-bound workload.
- Increasing the number of threads improved the measured I/O-bound workload time.
- Processes had higher overhead in these particular tests.

These observations apply to the tested workloads and computer. Results can vary depending on hardware, operating system, Python version and workload.

## 8. Conclusion

The experiment demonstrates that threads and processes have different performance characteristics.

Threads had lower creation overhead in this experiment and performed well for the tested I/O-bound workload. Processes had higher creation overhead, but process-based parallelism can be useful for CPU-intensive workloads where multiple CPU cores can be used independently.

The appropriate approach depends on the workload and the performance requirements.

## 9. Results File

The raw benchmark measurements are available in:

`results/benchmark_results.csv`
