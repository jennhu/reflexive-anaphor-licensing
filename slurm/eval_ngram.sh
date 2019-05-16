#!/bin/sh
echo "Model = ngram"
bash /om/group/cpl/language-models/scripts/eval_ngram.sh \
    /om/user/jennhu/rnng-refl/materials/$1_sentences_uncased.txt \
    /om/user/jennhu/rnng-refl/surprisal_data/5gram/$1_surprisal_5gram.txt
