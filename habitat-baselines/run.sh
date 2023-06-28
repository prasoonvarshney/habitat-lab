#!/bin/bash

export MAGNUM_LOG=verbose 
export MAGNUM_GPU_VALIDATION=ON

rm -rf /home/ubuntu/habitat-exp/habitat-lab/video_dir/*.mp4

python3 -u -m habitat_baselines.run \
  --config-name=rearrange/rl_hierarchical_oracle_nav.yaml \
  habitat_baselines.evaluate=True \
  habitat_baselines/rl/policy=hl_fixed \
  habitat_baselines/rl/policy/hierarchical_policy/defined_skills=oracle_skills