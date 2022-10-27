from d_utils.ddpg import DDPG
from d_utils.memory import Memory

import gym
import gym.wrappers.monitoring.video_recorder

import numpy as np
import torch


def main():
    env = gym.make("HalfCheetahCustom-v0", render_mode="rgb_array")

    action_space = env.action_space.shape[0]
    state_space = env.observation_space.shape[0]

    model = DDPG(state_space, action_space)

    if str(model.device) != "cuda:0":
        print("\nTHIS WILL TAKE SUPER DUPER LONG WITHOUT CUDA, PLEASE USE A CUDA-CAPABLE DEVICE")
        print("\n\n\n... but if you insist....\n")
        


    MAX_ITERATIONS = 50
    LOGGING_ITERATIONS = 10 
    learning = []
    memory = Memory()

    for i in range(1, MAX_ITERATIONS + 1):
        done = False
        cumulative_rewards = 0

        state, _ = env.reset()

        if i%LOGGING_ITERATIONS == 0:
            rec = gym.wrappers.monitoring.video_recorder.VideoRecorder(env, f"cheetah_vids/{i}.mp4")

        steps = 0
        
        while not done:
            action = model.predict(np.expand_dims(state, axis=0))

            new_state, rewards, done, *_ = env.step(action)

            memory.push((state, action, rewards, new_state, done))

            state = new_state

            if i%LOGGING_ITERATIONS == 0: 
                rec.capture_frame()
            cumulative_rewards += rewards

            steps += 1
            if steps % 50 == 0:
                for _ in range(50):
                    model.update(memory, 256)

        learning.append(cumulative_rewards)
        model.update_randomness() # decay randomness of model
        

        if i%LOGGING_ITERATIONS == 0:
            rec.close()
            print(f"Iteration: {i} | Moving-Average Reward: {np.mean(learning[-LOGGING_ITERATIONS:]):.4f}")


if __name__ == "__main__":
    main()
