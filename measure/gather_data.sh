#!/bin/sh
parent_path=$( cd "$(dirname "${BASH_SOURCE}")" ; pwd -P )

cd "$parent_path"
# Gathering of data
# For 3PR (PSwap 0, 0.25, 0.5, 0.75, 1)
./../gather_data.py -f config-3PR-measure.yml -k swap_prob  -min 0 -max 1 -n 0.25 -m NdcgEval -t offline_test -o all_evals_swap_prob_n0.25

# For D3PR
./../gather_data.py -f config-D3PR-measure.yml -min 0 -max 1 -n 1 -m NdcgEval -t offline_test -o all_evals -k trail

# For DBGD
./../gather_data.py -f config-DBGD-measure.yml -min 0 -max 1 -n 1 -m NdcgEval -t offline_test -o all_evals -k trail

