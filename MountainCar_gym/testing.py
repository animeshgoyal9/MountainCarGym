# !/usr/bin/env python
# -*- coding: utf-8 -*-

# import gym
# import MountainCar

# from stable_baselines.common.policies import MlpPolicy, MlpLstmPolicy
# from stable_baselines.common.vec_env import DummyVecEnv
# # from stable_baselines.deepq.policies import MlpPolicy
# from stable_baselines import PPO2, DQN
# from stable_baselines import results_plotter

# # env = gym.make('rcrs_gym_animesh-v0')

#     # env.render()
# env = gym.make('MountainCar-v1')
# env = DummyVecEnv([lambda: env])  # The algorithms require a vectorized environment to run

# model = PPO2(MlpPolicy, env, verbose=1, tensorboard_log = "./ppo2_falldown_tensorboard/")
# # model = DQN(MlpPolicy, env, verbose =1, tensorboard_log = "./ppo2_falldown_tensorboard/")
# # model = PPO2(MlpLstmPolicy, env, verbose=1, nminibatches = 1, tensorboard_log = "./ppo2_rcrs_animesh_tensorboard/")
# model.learn(total_timesteps=10000)
# obs = env.reset()
# total_rewards = 0
# for i in range(100000):
#     action, _states = model.predict(obs)
#     obs, rewards, dones, info = env.step(action)
#     total_rewards += rewards
#     print(total_rewards)
#     print(i)
#     print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")

import gym
import MountainCar

from stable_baselines.common.policies import MlpPolicy, MlpLstmPolicy
from stable_baselines.common.vec_env import DummyVecEnv
# from stable_baselines.deepq.policies import MlpPolicy
from stable_baselines import PPO2, DQN
from stable_baselines import results_plotter
from stable_baselines.bench import Monitor
from stable_baselines.results_plotter import load_results, ts2xy
from stable_baselines import DDPG
from stable_baselines.ddpg import AdaptiveParamNoiseSpec

import os
import numpy as np
import matplotlib.pyplot as plt


best_mean_reward, n_steps = -np.inf, 0
def callback(_locals, _globals):
    global n_steps, best_mean_reward
    # Print stats every 1000 calls
    if (n_steps + 1) % 1000 == 0:
# Evaluate policy training performance
        x, y = ts2xy(load_results(log_dir), 'timesteps')
        if len(x) > 0:
            mean_reward = np.mean(y[-100:])
            print(x[-1], 'timesteps')
            print("Best mean reward: {:.2f} - Last mean reward per episode: {:.2f}".format(best_mean_reward, mean_reward))
            # New best model, you could save the agent here
            if mean_reward > best_mean_reward:
                best_mean_reward = mean_reward
                # Example for saving best model
                print("Saving new best model")
                _locals['self'].save(log_dir + 'best_model.pkl')
    n_steps += 1
    return True


# Create log dir
log_dir = "/u/animesh9/Desktop/gRPC/MountainCar_gym/tmp/gym/"
os.makedirs(log_dir, exist_ok=True)
# Create and wrap the environment
env = gym.make('MountainCar-v1')
env = Monitor(env, log_dir, allow_early_resets=True)
env = DummyVecEnv([lambda: env])  # The algorithms require a vectorized environment to run
# Add some param noise for exploration
param_noise = AdaptiveParamNoiseSpec(initial_stddev=0.1, desired_action_stddev=0.1)
# Because we use parameter noise, we should use a MlpPolicy with layer normalization
model = PPO2(MlpPolicy, env, verbose=1, tensorboard_log = "./ppo2_falldown_tensorboard/")
# Train the agent
model.learn(total_timesteps=int(1000000), callback=callback)
obs = env.reset()
for i in range(100000):
    action, _states = model.predict(obs)
    obs, rewards, dones, info = env.step(action)
    print("Rewards: ", rewards)
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")