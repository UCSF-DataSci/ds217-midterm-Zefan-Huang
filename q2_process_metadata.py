#!/usr/bin/env python3
# Assignment 5, Question 2: Python Data Processing
# Process configuration files for data generation.
import random

def parse_config(filepath: str) -> dict:
    """
    Parse config file (key=value format) into dictionary.

    Args:
        filepath: Path to q2_config.txt

    Returns:
        dict: Configuration as key-value pairs

    Example:
        >>> config = parse_config('q2_config.txt')
        >>> config['sample_data_rows']
        '100'
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
    Validate configuration values using if/elif/else logic.

    Rules:
    - sample_data_rows must be an int and > 0
    - sample_data_min must be an int and >= 1
    - sample_data_max must be an int and > sample_data_min

    Args:
        config: Configuration dictionary

    Returns:
        dict: Validation results {key: True/False}

    Example:
        >>> config = {'sample_data_rows': '100', 'sample_data_min': '18', 'sample_data_max': '75'}
        >>> results = validate_config(config)
        >>> results['sample_data_rows']
        True
    """
    result = {}
    if 'sample_data_rows' in config:
        if config['sample_data_rows'].isdigit() and int(config['sample_data_rows']) > 0:
            result['sample_data_rows'] = True
        else:
            result['sample_data_rows'] = False
    else:
        result['sample_data_rows'] = False
    
    if 'sample_data_min' in config:
        if config['sample_data_min'].isdigit() and int(config['sample_data_min']) >= 1:
            result['sample_data_min'] = True
        else:
            result['sample_data_min'] = False
    else:
        result['sample_data_min'] = False
    if 'sample_data_max' in config and 'sample_data_min' in config:
        if (config['sample_data_max'].isdigit() and 
            int(config['sample_data_max']) > int(config['sample_data_min'])):
            result['sample_data_max'] = True
        else:
            result['sample_data_max'] = False
    else:
        result['sample_data_max'] = False
    return result


def generate_sample_data(filename: str, config: dict) -> None:
    """
    Generate a file with random numbers for testing, one number per row with no header.
    Uses config parameters for number of rows and range.

    Args:
        filename: Output filename (e.g., 'sample_data.csv')
        config: Configuration dictionary with sample_data_rows, sample_data_min, sample_data_max

    Returns:
        None: Creates file on disk

    Example:
        >>> config = {'sample_data_rows': '100', 'sample_data_min': '18', 'sample_data_max': '75'}
        >>> generate_sample_data('sample_data.csv', config)
        # Creates file with 100 random numbers between 18-75, one per row
        >>> import random
        >>> random.randint(18, 75)  # Returns random integer between 18-75
    """
    rows = int(config.get('sample_data_rows', 0))
    min_val = int(config.get('sample_data_min', 0))
    max_val = int(config.get('sample_data_max', 0))
    
    with open(filename, 'w') as f:
        for _ in range(rows):
            number = random.randint(min_val, max_val)
            f.write(f"{number}\n")


def calculate_statistics(data: list) -> dict:
    """
    Calculate basic statistics.

    Args:
        data: List of numbers

    Returns:
        dict: {mean, median, sum, count}

    Example:
        >>> stats = calculate_statistics([10, 20, 30, 40, 50])
        >>> stats['mean']
        30.0
    """
    result = []
    for i in data:
        result.append(int(i))
    total = sum(result)
    count = len(result)
    mean = sum(result) / len(result)
    sorted_result = sorted(result)
    if len(result) % 2 == 0:
         median = (sorted_result[len(result) // 2 - 1] + sorted_result[len(result) // 2]) / 2
    else:
        median = sorted(result)[len(result) // 2]

    total = sum(result)
    count = len(result)
    return {'mean': mean, 'median': median, 'sum': total, 'count': count}


if __name__ == '__main__':
    # TODO: Test your functions with sample data
    # Example:
    # config = parse_config('q2_config.txt')
    # validation = validate_config(config)
    # generate_sample_data('data/sample_data.csv', config)
    # 
    sample = ['10', '20', '30', '40', '50']
    print(calculate_statistics(sample))