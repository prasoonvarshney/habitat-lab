#!/bin/bash


export MAGNUM_LOG=quiet 
export HABITAT_SIM_LOG=quiet
export MAGNUM_GPU_VALIDATION=OFF

set -x

python -u -m habitat_baselines.run \
    --config-name=rearrange/rl_skill.yaml \
    benchmark/rearrange=place