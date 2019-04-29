#!/bin/bash

python plot_surprisals.py -exp "loc_himself" -model all -o plots/vs_baseline/ -vs & \
python plot_surprisals.py -exp "loc_herself" -model all -o plots/vs_baseline/ -vs & \
python plot_surprisals.py -exp "loc_pl" -model all -o plots/vs_baseline/ -vs & \
python plot_surprisals.py -exp "cc_himself" -model all -o plots/vs_baseline/ -vs & \
python plot_surprisals.py -exp "cc_herself" -model all -o plots/vs_baseline/ -vs & \
python plot_surprisals.py -exp "cc_pl" -model all -o plots/vs_baseline/ -vs & \
python plot_surprisals.py -exp "cc_agree" -model all -o plots/vs_baseline/ -vs & \
python plot_surprisals.py -exp "cc_agree_pl" -model all -o plots/vs_baseline/ -vs & \
wait