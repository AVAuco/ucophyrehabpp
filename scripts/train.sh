#!/bin/bash

echo "Starting sequential execution of training process"

python -m src.cli.train experiment=sample_experiment

echo "Training process finished."