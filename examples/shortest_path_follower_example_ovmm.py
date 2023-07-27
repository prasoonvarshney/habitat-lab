#!/usr/bin/env python3

# Copyright (c) Meta Platforms, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import os
import shutil
import json
import numpy as np

import habitat
from habitat.core.utils import try_cv2_import
from habitat.tasks.nav.shortest_path_follower import ShortestPathFollower
from habitat.utils.visualizations import maps
from habitat.utils.visualizations.utils import images_to_video

cv2 = try_cv2_import()

IMAGE_DIR = os.path.join("examples", "images")
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)


class SimpleRLEnv(habitat.RLEnv):
    def get_reward_range(self):
        return [-1, 1]

    def get_reward(self, observations):
        return 0

    def get_done(self, observations):
        return self.habitat_env.episode_over

    def get_info(self, observations):
        return self.habitat_env.get_metrics()


def draw_top_down_map(info, output_size):
    return maps.colorize_draw_agent_and_fit_to_height(
        info["top_down_map"], output_size
    )


def shortest_path_example():
    config = habitat.get_config(
        config_path="benchmark/ovmm/ovmm.yaml",
        overrides=[
            "+habitat/task/measurements@habitat.task.measurements.top_down_map=top_down_map"
        ],
    )

    with SimpleRLEnv(config=config) as env:
        print(f"Episode 0: {env.episodes[0]}")
        goal_radius = None  # env.episodes[0].goals[0].radius
        if goal_radius is None:
            goal_radius = config.habitat.simulator.forward_step_size
        follower = ShortestPathFollower(
            env.habitat_env.sim, goal_radius, False
        )

        print("Environment creation successful")
        for episode in range(3):
            env.reset()
            dirname = os.path.join(
                IMAGE_DIR, "shortest_path_ovmm", "%02d" % episode
            )
            if os.path.exists(dirname):
                shutil.rmtree(dirname)
            os.makedirs(dirname)
            print("Agent stepping around inside environment.")
            images = []
            steps, max_steps = 0, 1000
            print(f"Robot start location: {env.habitat_env.current_episode.start_position}")
            print(f"Robot start orientation: {env.habitat_env.current_episode.start_rotation}")
            
            # with open(os.path.join(dirname, f"ovmm_episode_{episode}.json"), "w") as f:
            #     json.dump(env.habitat_env.current_episode.candidate_objects[0], f, indent=4)
            
            print(f"\n\nCandidate objects:")
            for i, candidate_object in enumerate(env.habitat_env.current_episode.candidate_objects):
                print(f"Candidate object {i}: (position={candidate_object.position}, object_name={candidate_object.object_name}, object_category={candidate_object.object_category})")
            print(f"\n\nStart receptacles:")
            for i, candidate_start_receptacle in enumerate(env.habitat_env.current_episode.candidate_start_receps):
                print(f"Candidate receptacle {i}: (position={candidate_start_receptacle.position}, object_name={candidate_start_receptacle.object_name}, object_category={candidate_start_receptacle.object_category})")

            print(f"\n\nTarget receptacles:")
            for i, candidate_goal_receptacle in enumerate(env.habitat_env.current_episode.candidate_goal_receps):
                print(f"Candidate receptacle {i}: (position={candidate_goal_receptacle.position}, object_name={candidate_goal_receptacle.object_name}, object_category={candidate_goal_receptacle.object_category})")

            target_location = env.habitat_env.current_episode.candidate_objects[0].position
            print(f"Target locations for episode {episode}:")
            print(f"Object: {target_location}")
            print(f"Start: {env.habitat_env.current_episode.candidate_start_receps[0].position}")
            print(f"Target: {env.habitat_env.current_episode.candidate_goal_receps[0].position}")


            while not env.habitat_env.episode_over and steps < max_steps:
                best_action = follower.get_next_action(
                    target_location,
                )
                if best_action is None:
                    break

                observations, reward, done, info = env.step(best_action)
                steps += 1
                im = observations["robot_head_rgb"]
                top_down_map = draw_top_down_map(info, im.shape[0])
                output_im = np.concatenate((im, top_down_map), axis=1)
                images.append(output_im)
            images_to_video(images, dirname, "trajectory")
            print("Episode finished")


def main():
    shortest_path_example()


if __name__ == "__main__":
    main()
