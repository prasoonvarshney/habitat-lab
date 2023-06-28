#!/bin/bash


export MAGNUM_LOG=quiet 
export HABITAT_SIM_LOG=quiet
export MAGNUM_GPU_VALIDATION=OFF

set -x

python -u -m habitat_baselines.run \
    --config-name=rearrange/rl_skill.yaml \
    benchmark/rearrange=pick \
    habitat_baselines.rl.ver.variable_experience=False \
    habitat_baselines.rl.ver.num_inference_workers=1