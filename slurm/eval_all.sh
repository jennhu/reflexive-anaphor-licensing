#!/bin/sh
$EXP=$1
sbatch eval_grnn.batch $EXP
sbatch eval_jrnn.batch $EXP
sbatch eval_rnng.batch $EXP
sbatch eval_trans.batch $EXP