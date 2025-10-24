#!/usr/bin/env python3
# Assignment 5, Question 2: Python Data Processing
# Process configuration files for data generation.
import random
import os
import statistics
from typing import List, Dict, Any

def parse_config(filepath: str) -> dict:
    """
    Parse key=value config file into a dict.
    """
    config = {}
    with open(filepath, 'r') as file:
        for line in file:
            line = line.strip()
            if line and '=' in line:
                key, value = line.split('=', 1)
                config[key.strip()] = value.strip()
    return config

def validate_config(config: dict) -> dict:
    """
    Validate configuration values.
    Rules:
      - sample_data_rows must be int > 0
      - sample_data_min must be int >= 1
      - sample_data_max must be int > sample_data_min
    Returns dict of booleans for each key.
    """
    result = {}
    if 'sample_data_rows' in config:
        if str(config['sample_data_rows']).isdigit() and int(config['sample_data_rows']) > 0:
            result['sample_data_rows'] = True
        else:
            result['sample_data_rows'] = False
    else:
        result['sample_data_rows'] = False

    if 'sample_data_min' in config:
        if str(config['sample_data_min']).isdigit() and int(config['sample_data_min']) >= 1:
            result['sample_data_min'] = True
        else:
            result['sample_data_min'] = False
    else:
        result['sample_data_min'] = False

    if 'sample_data_max' in config and 'sample_data_min' in config:
        if (str(config['sample_data_max']).isdigit() and
            int(config['sample_data_max']) > int(config['sample_data_min'])):
            result['sample_data_max'] = True
        else:
            result['sample_data_max'] = False
    else:
        result['sample_data_max'] = False

    return result

def generate_sample_data(filename: str, config: dict) -> None:
    """
    Generate a file with random integers, one per line, no header.
    """
    rows = int(config.get('sample_data_rows', 0))
    min_val = int(config.get('sample_data_min', 0))
    max_val = int(config.get('sample_data_max', 0))

    # Ensure target directory exists
    os.makedirs(os.path.dirname(filename) or '.', exist_ok=True)

    with open(filename, 'w') as f:
        for _ in range(rows):
            number = random.randint(min_val, max_val)
            f.write(f"{number}\n")

def calculate_statistics(data: List[Any]) -> Dict[str, Any]:
    """
    Calculate mean, median, sum, count from a list of numbers or numeric strings.
    """
    if not data:
        return {'mean': 0.0, 'median': 0.0, 'sum': 0, 'count': 0}

    nums = [int(x) for x in data]
    total = sum(nums)
    count = len(nums)
    mean = total / count
    median = statistics.median(nums)
    return {'mean': mean, 'median': median, 'sum': total, 'count': count}

if __name__ == '__main__':
    # Quick CLI: parse config and generate sample data for grading
    import os
    
    cfg_path = 'q2_config.txt'
    if os.path.exists(cfg_path):
        cfg = parse_config(cfg_path)
        validation = validate_config(cfg)

        if all(validation.values()):
            os.makedirs('data', exist_ok=True)
            generate_sample_data('data/sample_data.csv', cfg)
            print("Generated data/sample_data.csv")
        else:
            print("Invalid config:", validation)
    else:
        # Demo run (safe numeric example)
        sample = [10, 20, 30, 40, 50]
        print(calculate_statistics(sample))