#!/bin/bash
STIMPATH="/om/user/jennhu/rnng-refl/materials/stimuli/embed"
SURPRISALPATH="/om/user/jennhu/rnng-refl/surprisal_data/grnn/embed"
STIMULI=($(ls -1 ${STIMPATH}))
cd /om/user/jennhu/colorlessgreenRNNs/src/language_models
for stim in ${STIMULI[@]}
do
    echo ${stim}
    python evaluate_target_word_test.py --data ../../data/wiki \
    --checkpoint ../../hidden650_batch128_dropout0.2_lr20.0.pt \
    --prefixfile ${STIMPATH}/${stim} --surprisalmode True \
    --outf ${SURPRISALPATH}/${stim}
done