# !/usr/bin/env python
# -*- coding: utf-8 -*-

import gym
import MountainCar

from stable_baselines.common.policies import MlpPolicy, MlpLstmPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import PPO2

# env = gym.make('rcrs_gym_animesh-v0')

    # env.render()
env = gym.make('MountainCar-v1')
env = DummyVecEnv([lambda: env])  # The algorithms require a vectorized environment to run

model = PPO2(MlpPolicy, env, verbose=1, tensorboard_log = "./ppo2_falldown_tensorboard/")
# model = PPO2(MlpLstmPolicy, env, verbose=1, nminibatches = 1, tensorboard_log = "./ppo2_rcrs_animesh_tensorboard/")
model.learn(total_timesteps=10000)
obs = env.reset()
for i in range(100000):
	action, _states = model.predict(obs)
	obs, rewards, dones, info = env.step(action)
	print(action)
	print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")