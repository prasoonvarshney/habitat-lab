#!/bin/bash


export MAGNUM_LOG=verbose 
export MAGNUM_GPU_VALIDATION=ON

python3 -u -m habitat_baselines.run \
  --config-name=rearrange/rl_hierarchical.yaml \
  habitat_baselines.evaluate=False \
  habitat_baselines/rl/policy/hierarchical_policy/defined_skills=oracle_skills