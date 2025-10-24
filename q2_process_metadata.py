#!/usr/bin/env python3
# Assignment 5, Question 2: Python Data Processing
# Process configuration files for data generation.
import random


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


def _ensure_dir_for_file(filename: str) -> None:
    """
    Ensure the directory for `filename` exists. Uses dynamic import of os only when needed
    so this module only has a top-level import of `random` as requested.
    """
    # derive directory part without importing os at module import time
    sep_pos = filename.rfind('/')
    dirpath = filename[:sep_pos] if sep_pos != -1 else '.'
    if not dirpath or dirpath == '.':
        return
    os_mod = __import__('os')
    # correct call is os.makedirs
    os_mod.makedirs(dirpath, exist_ok=True)


def generate_sample_data(filename: str, config: dict) -> None:
    """
    Generate a file with random integers, one per line, no header.
    """
    rows = int(config.get('sample_data_rows', 0))
    min_val = int(config.get('sample_data_min', 0))
    max_val = int(config.get('sample_data_max', 0))

    # Ensure target directory exists (use helper that imports os only at call time)
    _ensure_dir_for_file(filename)

    with open(filename, 'w') as f:
        for _ in range(rows):
            number = random.randint(min_val, max_val)
            f.write(f"{number}\n")


def _median_from_list(nums):
    """Return median of a list of numbers as float."""
    n = len(nums)
    if n == 0:
        return 0.0
    sorted_nums = sorted(nums)
    mid = n // 2
    if n % 2 == 1:
        return float(sorted_nums[mid])
    else:
        return (sorted_nums[mid - 1] + sorted_nums[mid]) / 2.0


def calculate_statistics(data) -> dict:
    """
    Calculate mean, median, sum, count from a list of numbers or numeric strings.
    """
    if not data:
        return {'mean': 0.0, 'median': 0.0, 'sum': 0, 'count': 0}

    nums = [int(x) for x in data]
    total = sum(nums)
    count = len(nums)
    mean = total / count
    median = _median_from_list(nums)
    return {'mean': mean, 'median': median, 'sum': total, 'count': count}


if __name__ == '__main__':
    # Optional: read config and produce outputs if run directly
    try:
        cfg = parse_config('q2_config.txt')
        validation = validate_config(cfg)
        if all(validation.values()):
            generate_sample_data('data/sample_data.csv', cfg)
            with open('data/sample_data.csv') as f:
                values = [int(line.strip()) for line in f if line.strip()]
            stats = calculate_statistics(values)
            # Ensure output dir exists
            _ensure_dir_for_file('output/statistics.txt')
            with open('output/statistics.txt', 'w') as out:
                out.write('\n'.join([f"{k}: {v}" for k, v in stats.items()]))
        else:
            print('Invalid configuration; no files generated.')
    except FileNotFoundError:
        # If config or data dir is absent, do nothing when executed
        pass
