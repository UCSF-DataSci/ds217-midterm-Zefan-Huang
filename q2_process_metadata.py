#!/usr/bin/env python3
# Assignment 5, Question 2: Python Data Processing
# Process configuration files for data generation.
import random


def parse_config(filepath: str) -> dict:
    config = {}
    with open(filepath, 'r') as file:
        for line in file:
            line = line.strip()
            if line and '=' in line:
                key, value = line.split('=', 1)
                config[key.strip()] = value.strip()
    return config


def validate_config(config: dict) -> dict:
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
    rows = int(config.get('sample_data_rows', 0))
    min_val = int(config.get('sample_data_min', 0))
    max_val = int(config.get('sample_data_max', 0))

    with open(filename, 'w') as f:
        for _ in range(rows):
            number = random.randint(min_val, max_val)
            f.write(f"{number}\n")


def calculate_statistics(data: list) -> dict:
    nums = [int(x) for x in data]
    nums.sort()

    total = sum(nums)
    count = len(nums)
    mean = total / count

    if count % 2 == 0:
        median = (nums[count // 2 - 1] + nums[count // 2]) / 2
    else:
        median = nums[count // 2]

    return {'mean': mean, 'median': median, 'sum': total, 'count': count}


if __name__ == '__main__':
    config = parse_config('q2_config.txt')
    validation = validate_config(config)

    if not all(validation.values()):
        print("Configuration invalid. Please fix q2_config.txt and re-run.")
        print("Validation results:", validation)
        exit(1)

    output_file = 'data/sample_data.csv'
    generate_sample_data(output_file, config)

    with open(output_file, 'r') as f:
        data = f.read().splitlines()

    stats = calculate_statistics(data)

    with open('output/statistics.txt', 'w') as f:
        for key, value in stats.items():
            f.write(f"{key}: {value}\n")

    print("Statistics saved to output/statistics.txt")


