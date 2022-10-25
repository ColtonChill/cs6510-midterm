import random
from collections import deque

import numpy as np

class Memory:
    def __init__(self, max_size=100):
        self.memory=deque(maxlen=max_size)

    def push(self, element):
        self.memory.append(element)

    def get_batch(self, batch_size=4):
        idx = np.random.permutation(len(self.memory))[:batch_size]
        state = []
        action = []
        reward = []
        next = []
        done = []
        for i in idx:
            s, a, r, sp, d, = self.memory[i]
            state.append(s)
            action.append(a)
            reward.append(r)
            next.append(sp)
            done.append(d)
        state = np.array(state)
        action = np.array(action)
        reward = np.array(reward)
        next = np.array(next)
        done = np.array(done)

        return state, action, reward, next, done

    def __repr__(self):
        return f"Current memory: {len(self.memory)} elements"

    def __len__(self):
        return len(self.memory)
