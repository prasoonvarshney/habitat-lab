#!/bin/bash


export MAGNUM_LOG=verbose 
export MAGNUM_GPU_VALIDATION=ON

python3 -u -m habitat_baselines.run \
  --config-name=rearrange/rl_rearrange_easy.yaml \
  habitat_baselines.evaluate=False