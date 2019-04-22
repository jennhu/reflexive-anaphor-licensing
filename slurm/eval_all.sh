#!/bin/sh

# expected usage: ./eval_all.sh <experiment name>
MODELS=("grnn" "jrnn" "rnng" "tiny" "trans")
for model in ${MODELS[@]}
do
    echo "Model = $model"
    sbatch eval_$model.batch $1
done