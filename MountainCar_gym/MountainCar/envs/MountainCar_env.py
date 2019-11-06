
from __future__ import print_function
import logging

import grpc

import PyRL_pb2
import PyRL_pb2_grpc

import os, subprocess, time, signal
import gym, numpy as np
from gym import error, spaces
from gym import utils
from gym.utils import seeding
import logging, random
import socket, pickle, json, subprocess, ast
from subprocess import *
import numpy as np
import threading
import time, math

MAX_TIMESTEP = 1000

action_set_list = np.array([-1, 0, 1], dtype = object)

class MountainCarenv(gym.Env):
    metadata = {'render.modes' : None}
    x = 0
    v = 0   
    current_action = 0
    def __init__(self):
        
        self.goal_position = 50
        self.goal_velocity = 0
        self.action_space = spaces.Discrete(len(action_set_list))
        
        low = np.array([-120, -7])
        high = np.array([50, 7])
        
        self.observation_space = spaces.Box(low, high, dtype=np.float32, shape=None)

        self.curr_episode = 0
        self.seed()


    def step(self, action):
        current_action = action
        
        self.curr_episode += 1
        reward = -1
        self.current_action = action
        logging.basicConfig()
        self.x, self.v = run(action)
        print("Current Action: ", self.current_action)
        print("Current Location: ", self.x, ", ", self.v)

        if (self.x >= 50):
            self.state = (0, 0)
        elif (self.x <= -120):
            self.state = (-120,0)
        else:
            self.state = (self.x, self.v)

        done = bool(self.x >= 49 or self.curr_episode == MAX_TIMESTEP)
        return np.array(self.state), reward, done , {}

    def reset(self):
        self.curr_episode = 0
        self.x = -50
        self.v = 0
        self.state = (self.x, self.v)
        return np.array(self.state) 

    def seed(self, seed = None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

def run(a):
    with grpc.insecure_channel('localhost:9090') as channel:
        print("Connecting to Server..")
        stub = PyRL_pb2_grpc.PyRLStub(channel)
        response = stub.getObs(PyRL_pb2.Action(action=action_set_list[a]))
        x = response.x
        v = response.v
    print("PyServer client received - ", x, ", ", v)
    time.sleep(0.05)
    return x, v


# class MountainCarenv(gym.Env):
#     metadata = {
#         'render.modes': ['human', 'rgb_array'],
#         'video.frames_per_second': 30
#     }

#     def __init__(self, goal_velocity = 0):
#         self.min_position = -1.2
#         self.max_position = 0.6
#         self.max_speed = 0.07
#         self.goal_position = 0.5
#         self.goal_velocity = goal_velocity
#         self.curr_episode = 0
#         self.force=0.001
#         self.gravity=0.0025

#         self.low = np.array([self.min_position, -self.max_speed])
#         self.high = np.array([self.max_position, self.max_speed])

#         self.viewer = None

#         self.action_space = spaces.Discrete(3)
#         self.observation_space = spaces.Box(self.low, self.high, dtype=np.float32)

#         self.seed()

#     def seed(self, seed=None):
#         self.np_random, seed = seeding.np_random(seed)
#         return [seed]

#     def step(self, action):
#         assert self.action_space.contains(action), "%r (%s) invalid" % (action, type(action))
#         self.curr_episode += 1

#         position, velocity = self.state
#         velocity += (action-1)*self.force + math.cos(3*position)*(-self.gravity)
#         velocity = np.clip(velocity, -self.max_speed, self.max_speed)
#         position += velocity
#         position = np.clip(position, self.min_position, self.max_position)
#         if (position==self.min_position and velocity<0): velocity = 0

#         done = bool(position >= self.goal_position or self.curr_episode == MAX_TIMESTEP)
#         reward = -1.0

#         self.state = (position, velocity)
#         return np.array(self.state), reward, done, {}

#     def reset(self):
#         self.curr_episode = 0
#         self.state = np.array([self.np_random.uniform(low=-0.6, high=-0.4), 0])
#         return np.array(self.state)