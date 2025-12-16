#!/bin/bash

echo "Generating manifests.."
 
python -m src.cli.build_manifest experiment=sample_experiment

echo "Process finished."