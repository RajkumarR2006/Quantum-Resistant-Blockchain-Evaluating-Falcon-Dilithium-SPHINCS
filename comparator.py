# comparator.py

import json
from tests.benchmark import main as run_benchmark

def main():
    print("Running signature benchmarks...")
    run_benchmark()
    # You may expand: collect metrics (key size, sig. size, verify time etc.) and save as JSON

if __name__ == "__main__":
    main()
