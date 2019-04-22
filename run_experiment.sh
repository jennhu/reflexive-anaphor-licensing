#!/bin/sh

echo "Processing materials for $1"
python process_materials.py $1

cd slurm
./eval_all $1