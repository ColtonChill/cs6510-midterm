# class PID:
#     def __init__(self,P,I,D):
#         self.p=P
#         self.i=I
#         self.d=D
#         self.integral=0
#         self.prev=0
    
#     def __call__(self,err,dt=0.2):
#         result = self.p*err + (self.d*(err-self.prev))/dt + self.i*self.integral
#         self.prev = err
#         self.integral = self.integral + err
#         return result

import gym
from tqdm import tqdm
from time import sleep
#* No longer do we need the reinforced learner
# from agent import Cartpole_Agent
from cartpoleEnv import CartPoleEnv
from random import randint
#* Instead, we'll use an explicit controller
from simple_pid import PID
from math import pi

# Change the proportional gain to [5,10] because we want a snappy response.
# Leave the integrator and derivative at 1 so we avoid both stead-state and overshoot error.
pid = PID(10,1,1)

env = CartPoleEnv(render_mode="human")  # rgb_array

reward_arr = []
for i in tqdm(range(2)):
    (x, x_dot, theta, theta_dot), done = env.reset()
    while not done:
        # Raw Radians are small, so we give that part a bit of a boost
        err = x+ theta*10
        action = pid(err)
        # print('err:',round(err,3),'action:', round(action,3))
        action = int(action<=0)
        (x, x_dot, theta, theta_dot), reward, done, truncated, _ = env.step(action)
        # sleep(0.001)
