#!/bin/bash

echo "Starting sequential execution of test process"

python -m src.cli.test experiment=sample_experiment

echo "Test process finished."