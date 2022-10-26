import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import os

class Actor(nn.Module):
    def __init__(self, state_space, action_space):
        super(Actor, self).__init__()
        
        self.layer1 = nn.Linear(state_space, 128)
        self.layer2 = nn.Linear(128, 300)
        self.layer3 = nn.Linear(300, 400)
        self.layer4 = nn.Linear(400, action_space)
        nn.init.uniform_(self.layer4.weight, -3*1e-3, 3*1e-3)

        self.batch1 = nn.BatchNorm1d(128)
        self.batch2 = nn.BatchNorm1d(300)
        self.batch3 = nn.BatchNorm1d(400)

    def forward(self, x):
        self.eval()
        x = self.batch1(F.relu(self.layer1(x)))
        x = self.batch2(F.relu(self.layer2(x)))
        x = self.batch3(F.relu(self.layer3(x)))

        return torch.tanh(self.layer4(x))


class Critic(nn.Module):
    def __init__(self, state_space, action_space):
        super(Critic, self).__init__()

        self.layer1 = nn.Linear(state_space, 128)
        self.actionLayer1 = nn.Linear(action_space, 256)
        self.stateLayer1 = nn.Linear(128, 256)
        self.layer2 = nn.Linear(256, 300)
        self.layer3 = nn.Linear(300, 400)
        self.layer4 = nn.Linear(400, 1)

        self.batch1 = nn.BatchNorm1d(128)
        self.batch2 = nn.BatchNorm1d(256)

    def forward(self, state, action):
        self.eval()
        x = self.batch1(F.relu(self.layer1(state)))

        actOut = self.actionLayer1(F.relu(action))
        stOut = self.batch2(F.relu(self.stateLayer1(x)))
        combination = F.relu(actOut + stOut)
        out = F.relu(self.layer2(combination))
        out = F.relu(self.layer3(out))
        out = self.layer4(out)
        return out

class DDPG():
    def __init__(self, state_space, action_space):
        self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

        self.exploreDistribution = torch.distributions.normal.Normal(
            torch.zeros(action_space), torch.ones(action_space)
        )
        self.actor = Actor(state_space, action_space).to(self.device)
        self.critic = Critic(state_space, action_space).to(self.device)
        self.targetActor = Actor(state_space, action_space).to(self.device)
        self.targetCritic = Critic(state_space, action_space).to(self.device)
        self.critOptimizer = torch.optim.Adam(self.critic.parameters(), lr=1e-3, weight_decay=0.005)
        self.actOptimizer = torch.optim.Adam(self.actor.parameters(), lr=1e-4, weight_decay=0.005)
        self.loss = nn.MSELoss()
        self.gamma = 0.99
        self.rho = 0.001

    def predict(self, state):
        state = torch.from_numpy(state).float().to(self.device)
        pred = self.actor(state).detach()
        return pred.numpy()[0]

    def update(self, replay, batch_count):
        self.actor.train()
        self.critOptimizer.zero_grad()
        batch_sample = replay.get_batch(batch_count)
        state, action, reward, new_state, done = batch_sample
        state = torch.from_numpy(state).float().to(self.device)
        action = torch.from_numpy(action).float().to(self.device)
        reward = torch.from_numpy(reward).float().to(self.device)
        new_state = torch.from_numpy(new_state).float().to(self.device)
        done = torch.from_numpy(done).float().to(self.device)
        target = torch.unsqueeze(reward, 1)+torch.unsqueeze((1-done), 1)*self.gamma*(self.targetCritic(new_state, self.targetActor(new_state)))
        critic_loss = self.loss(target.detach(), self.critic(state, action))
        critic_loss.backward()
        self.critOptimizer.step()

        self.actOptimizer.zero_grad()
        policy_loss = -self.critic(state, self.actor(state)).mean()
        policy_loss.backward()
        self.actOptimizer.step()
        self._update_target()

    def _update_target(self):
        for i, j in zip(self.targetActor.parameters(), self.actor.parameters()):
            i.data *= (1-self.rho)
            i.data += self.rho*j.data
        for i, j in zip(self.targetCritic.parameters(), self.critic.parameters()):
            i.data *= (1-self.rho)
            i.data += self.rho*j.data

    def save(self, path='models/DDPG'):
        if 'models' in path and os.path.isdir('models') is False:
            os.mkdir('models')
        torch.save({'actor_weights': self.actor.state_dict(),
                    'critic_weights': self.critic.state_dict(),
                    'Critic_optimizer': self.critOptimizer.state_dict(),
                    'Actor_optimizer': self.actOptimizer.state_dict()
                   }, path)

        print(f"Model weights saved to {path}")

    def load(self, path='models/DDPG'):
        model = torch.load(path)
        self.actor.load_state_dict(model['actor_weights'])
        self.critic.load_state_dict(model['critic_weights'])
        self.critOptimizer.load_state_dict(model['Critic_optimizer'])
        self.actOptimizer.load_state_dict(model['Actor_optimizer'])

        print(f"Model weights loaded from {path}")
