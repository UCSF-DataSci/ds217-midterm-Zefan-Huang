#!/bin/bash

set -e 

echo "Setting up project directories..."

ROOT_DIR=$(pwd)

mkdir -p "$ROOT_DIR/data"\
         "$ROOT_DIR/output" \
         "$ROOT_DIR/reports"

echo "Directories created: data/, output/, reports/"

echo "Generating dataset...in"
echo "3"
sleep 1
echo "2"
sleep 1
echo "1"
sleep 1

python3 generate_data.py
echo "Dataset generated: data/clinical_trial_raw.csv"

tree "$ROOT_DIR" > "$ROOT_DIR/reports/directory_structure.txt"

echo "Directory structure saved to reports/directory_structure.txt"