#!/usr/bin/env python3
"""
CA2 starter benchmark: process creation vs thread creation.

Run on your own computer. Results are measurements from the current machine,
not pre-filled or simulated values.
"""
from __future__ import annotations

import argparse
import csv
import multiprocessing as mp
import os
import platform
import statistics
import threading
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True)

def cpu_task(n: int) -> int:
    total = 0
    for i in range(n):
        total += (i * i) % 997
    return total

def io_task(delay: float) -> int:
    time.sleep(delay)
    return 1

def thread_noop():
    return None

def process_noop():
    return None

def measure_creation(repeats: int) -> list[dict]:
    rows = []
    for kind in ("thread", "process"):
        samples = []
        for _ in range(repeats):
            start = time.perf_counter()
            if kind == "thread":
                worker = threading.Thread(target=thread_noop)
                worker.start()
                worker.join()
            else:
                # spawn is portable across Windows, macOS and Linux
                worker = mp.get_context("spawn").Process(target=process_noop)
                worker.start()
                worker.join()
            samples.append((time.perf_counter() - start) * 1_000_000)
        rows.append({
            "experiment": "creation",
            "workload": "no_op",
            "model": kind,
            "workers": 1,
            "repeats": repeats,
            "mean_time_ms": round(statistics.mean(samples) / 1000, 4),
            "mean_creation_us": round(statistics.mean(samples), 2),
            "stdev_creation_us": round(statistics.stdev(samples), 2) if len(samples) > 1 else 0,
        })
    return rows

def measure_workload(model: str, workload: str, workers: int,
                     tasks: int, cpu_iterations: int, io_delay: float,
                     repeats: int) -> dict:
    samples = []
    for _ in range(repeats):
        start = time.perf_counter()
        Executor = ThreadPoolExecutor if model == "thread" else ProcessPoolExecutor
        with Executor(max_workers=workers) as pool:
            if workload == "cpu":
                futures = [pool.submit(cpu_task, cpu_iterations) for _ in range(tasks)]
            else:
                futures = [pool.submit(io_task, io_delay) for _ in range(tasks)]
            for future in futures:
                future.result()
        samples.append(time.perf_counter() - start)
    return {
        "experiment": "workload",
        "workload": workload,
        "model": model,
        "workers": workers,
        "repeats": repeats,
        "mean_time_ms": round(statistics.mean(samples) * 1000, 3),
        "mean_creation_us": "",
        "stdev_creation_us": "",
    }

def main():
    parser = argparse.ArgumentParser(description="Compare process and thread overhead.")
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--tasks", type=int, default=8)
    parser.add_argument("--cpu-iterations", type=int, default=250_000)
    parser.add_argument("--io-delay", type=float, default=0.05)
    parser.add_argument("--workers", type=int, nargs="+", default=[1, 2, 4])
    args = parser.parse_args()

    if args.repeats < 1 or args.tasks < 1 or any(w < 1 for w in args.workers):
        parser.error("repeats, tasks and worker counts must be positive")

    rows = measure_creation(args.repeats)
    for workload in ("cpu", "io"):
        for model in ("thread", "process"):
            for workers in args.workers:
                rows.append(measure_workload(
                    model, workload, workers, args.tasks,
                    args.cpu_iterations, args.io_delay, args.repeats
                ))

    output = RESULTS / "benchmark_results.csv"
    fields = ["experiment", "workload", "model", "workers", "repeats",
              "mean_time_ms", "mean_creation_us", "stdev_creation_us"]
    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    print("CA2 Process vs Thread benchmark")
    print(f"System: {platform.platform()}")
    print(f"Python: {platform.python_version()} | CPU cores: {os.cpu_count()}")
    print(f"CSV saved to: {output}")
    print("\nMeasured results:")
    for row in rows:
        if row["experiment"] == "creation":
            print(f'{row["model"]:7} create+join: {row["mean_creation_us"]:>10} us')
        else:
            print(f'{row["workload"]:4} | {row["model"]:7} | '
                  f'{row["workers"]:2} workers | {row["mean_time_ms"]:>9} ms')

if __name__ == "__main__":
    mp.freeze_support()
    main()
