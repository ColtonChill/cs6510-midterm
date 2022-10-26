import numpy as np
import gym
from gym.wrappers import RecordVideo

import torch

import matplotlib.pyplot as plt
import seaborn as sns

class PolicyNN(torch.nn.Module):
    def __init__(self, obs_space, act_space):
        super(PolicyNN, self).__init__()
        self.layer1 = torch.nn.Linear(obs_space, 16)
        self.layer2 = torch.nn.Linear(16, act_space)

    def forward(self, x):
        x = self.layer1(x)

        x = torch.nn.functional.relu(x)

        x = self.layer2(x)

        x = torch.nn.functional.softmax(x, dim=1)
        return x


class Agent(object):
    def __init__(self, environment):
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.model = PolicyNN(environment.observation_space.shape[0], environment.action_space.n).to(self.device)
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=3e-3)

    def act(self, state):
        state = torch.from_numpy(state).float().unsqueeze(0).to(self.device)

        probs = self.model(state).cpu()

        m = torch.distributions.Categorical(probs)

        action = m.sample()

        return action.item(), m.log_prob(action)


if __name__ == "__main__":
    MAX_ITERATION = 1500
    LOG_ITERATION = 100

    environment = gym.wrappers.RecordVideo(
        gym.make("CartPole-v1", render_mode="rgb_array", max_episode_steps=500),
        video_folder="./videos",
        episode_trigger=lambda x: x==MAX_ITERATION-1
    )


    agent = Agent(environment)
    learning = []
    episode_count = 0

    for iteration in range(1, MAX_ITERATION+1):
        episode_count += 1
        steps = 0
        done = False
        state, _ = environment.reset()

        cumulative_rewards = 0
        action_probs = []

        while not done:
            steps += 1

            action, prob = agent.act(state)
            action_probs.append(prob)

            state, reward, done, *_ = environment.step(action)
            cumulative_rewards += reward

        loss = [-log_prob * cumulative_rewards for log_prob in action_probs]
        loss = torch.cat(loss).sum()

        agent.optimizer.zero_grad()
        loss.backward()
        agent.optimizer.step()

        learning.append(steps)

        if iteration % LOG_ITERATION == 0:
            print(f"Iteration: {iteration} | Moving-Average Steps: {np.mean(learning[-LOG_ITERATION:]):.4f}")


    x = np.arange(0, len(learning), 25)
    y = np.add.reduceat(learning, x) / 25

    sns.lineplot(x=x, y=y)
    plt.title("Cart Lifespan During Training")
    plt.xlabel("Episodes")
    plt.ylabel("Lifespan")
    plt.show()
