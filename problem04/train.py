from agent import Cartpole_Agent
from tqdm import tqdm
from random import randint
import matplotlib.pylab as plt
from cartpoleEnv import CartPoleEnv

env = CartPoleEnv(render_mode="rgb_array")
exp_replay_size = 256
agent = Cartpole_Agent(seed=randint(0,10000), 
                  layer_sizes=[env.observation_space.shape[0], 64, env.action_space.n], 
                  lr=1e-3, 
                  sync_freq=5,
                  exp_replay_size=exp_replay_size)

# Main training loop
losses_list, reward_list, episode_len_list, epsilon_list = [], [], [], []
episodes = 20000
epsilon = 1  # exploration rate

# initialize experience replay
index = 0
for i in range(exp_replay_size):
    obs, done = env.reset()
    while not done and index <= exp_replay_size:
        action = agent.get_action(obs, env.action_space.n, epsilon=1)
        obs_next, reward, done, truncated, _ = env.step(action.item())
        agent.collect_experience([obs, action.item(), reward, obs_next])
        obs = obs_next
        index += 1

index = 128
for i in tqdm(range(episodes)):
    (obs, done), losses, ep_len, rew = env.reset(), 0, 0, 0
    while not done:
        ep_len += 1
        action = agent.get_action(obs, env.action_space.n, epsilon)
        obs_next, reward, done, truncated, _ = env.step(action.item())
        agent.collect_experience([obs, action.item(), reward, obs_next])

        obs = obs_next
        rew += reward
        index += 1

        if index > 128:
            index = 0
            for j in range(4):
                loss = agent.train(batch_size=16)
                losses += loss
    if epsilon > 0.05: epsilon -= (1/10000 * 2)

    # track graphs
    losses_list.append(losses / ep_len)
    reward_list.append(rew)
    episode_len_list.append(ep_len)
    epsilon_list.append(epsilon)

    if i%200==0:
        fig, ((ax1,ax2),(ax3,ax4)) = plt.subplots(2,2, figsize=(15,8))
        ax1.plot(reward_list, color='g')
        ax1.set_title('Reward')
        ax2.plot(episode_len_list, color='gray')
        ax2.set_title('Time')
        ax3.plot(losses_list,color='r')
        ax3.set_title('Losses')
        ax4.plot(epsilon_list)
        ax4.set_title('Exportation rate')
        plt.savefig('plot.png')
        plt.close()

print("Saving trained model")
agent.save_trained_model("cartpole-model.pth")