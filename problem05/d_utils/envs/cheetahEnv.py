import numpy as np
import math

from gym import utils
from gym.envs.mujoco.mujoco_env import MuJocoPyEnv
from gym.spaces import Box

"""
This code taken from:

https://github.com/openai/gym/blob/master/gym/envs/mujoco/half_cheetah.py

Only the observation_space was changed in order to comply with pi movement on the hip motor
"""


class HalfCheetahEnv(MuJocoPyEnv, utils.EzPickle):
    metadata = {
        "render_modes": [
            "human",
            "rgb_array",
            "depth_array",
        ],
        "render_fps": 20,
    }

    def __init__(self, **kwargs):
        self.current_steps = 0
        observation_space = Box(
            low=np.array([-np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -math.pi, -np.inf, -np.inf, -np.inf, -np.inf]),
            high=np.array([np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, math.pi, np.inf, np.inf, np.inf, np.inf, ]), 
            dtype=np.float64)
        MuJocoPyEnv.__init__(
            self, "half_cheetah.xml", 5, observation_space=observation_space, **kwargs
        )
        utils.EzPickle.__init__(self, **kwargs)

    def step(self, action):
        xposbefore = self.sim.data.qpos[0]
        self.do_simulation(action, self.frame_skip)
        xposafter = self.sim.data.qpos[0]

        ob = self._get_obs()
        reward_ctrl = -0.1 * np.square(action).sum()
        reward_run = (xposafter - xposbefore) / self.dt
        reward = reward_ctrl + reward_run
        self.current_steps += 1
        terminated = self.current_steps > self.spec.max_episode_steps

        if self.render_mode == "human":
            self.render()
        return (
            ob,
            reward,
            terminated,
            False,
            dict(reward_run=reward_run, reward_ctrl=reward_ctrl),
        )

    def _get_obs(self):
        return np.concatenate(
            [
                self.sim.data.qpos.flat[1:],
                self.sim.data.qvel.flat,
            ]
        )

    def reset_model(self):
        qpos = self.init_qpos + self.np_random.uniform(
            low=-0.1, high=0.1, size=self.model.nq
        )
        qvel = self.init_qvel + self.np_random.standard_normal(self.model.nv) * 0.1
        self.current_steps = 0
        self.set_state(qpos, qvel)
        return self._get_obs()

    def viewer_setup(self):
        assert self.viewer is not None
        self.viewer.cam.distance = self.model.stat.extent * 0.5
