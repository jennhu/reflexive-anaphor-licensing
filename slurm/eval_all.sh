#!/bin/sh

# expected usage: ./eval_all.sh <experiment name>
MODELS=("grnn" "jrnn" "rnng" "tiny" "trans")
BIG_MODELS=("grnn" "jrnn" "trans")
for model in ${BIG_MODELS[@]}
do
    echo "Model = $model"
    sbatch eval_$model.batch $1
done