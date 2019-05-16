#!/bin/sh

# expected usage: ./eval_all.sh <experiment name>
MODELS=("grnn" "jrnn" "rnng" "tiny" "trans")
BIG_MODELS=("grnn" "jrnn" "trans")
for model in ${MODELS[@]}
do
    echo "Model = $model"
    sbatch eval_$model.batch $1
done

echo "Model = ngram"
bash /om/group/cpl/language-models/scripts/eval_ngram.sh \
    /om/user/jennhu/rnng-refl/materials/$1_sentences_uncased.txt \
    /om/user/jennhu/rnng-refl/surprisal_data/5gram_kn/$1_surprisal_5gram_kn.txt
