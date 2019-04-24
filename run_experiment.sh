#!/bin/sh

echo "Processing materials for $1"
python process_materials.py -exp $1

cd slurm
./eval_all.sh $1