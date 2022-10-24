import gym
from tqdm import tqdm
from time import sleep
from agent import Cartpole_Agent
from cartpoleEnv import CartPoleEnv
from random import randint

# env = gym.make('CartPole-v1', render_mode='human')
env = CartPoleEnv(render_mode="human")  # rgb_array

input_dim = env.observation_space.shape[0]
output_dim = env.action_space.n
exp_replay_size = 256
agent = Cartpole_Agent(seed=randint(0,10000), layer_sizes=[input_dim, 64, output_dim], lr=1e-3, sync_freq=5,
                  exp_replay_size=exp_replay_size)
agent.load_pretrained_model("cartpole-model.pth")

reward_arr = []
for i in tqdm(range(5)):
    (obs, done), rew = env.reset(), 0
    while not done:
        action = agent.get_action(obs, env.action_space.n, epsilon=0.01)
        obs, reward, done, truncated, _ = env.step(action.item())
        rew += reward
        sleep(0.01)

    reward_arr.append(rew)
print("average reward per episode :", sum(reward_arr) / len(reward_arr))
