#!/bin/bash

export MAGNUM_LOG=verbose 
export MAGNUM_GPU_VALIDATION=ON
export CUDA_LAUNCH_BLOCKING=1
export HYDRA_FULL_ERROR=1

rm -rf /home/ubuntu/habitat-exp/habitat-lab/video_dir/*.mp4

python3 -u -m habitat_baselines.run \
  --config-name=ovmm/ovmm_eval.yaml \
  habitat_baselines/rl/policy=hl_fixed \
  habitat_baselines/rl/policy/hierarchical_policy/defined_skills=oracle_skills