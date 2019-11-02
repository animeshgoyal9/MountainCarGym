
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



MAX_TIMESTEP = 300

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
        self.action_episode_memory = []
        self.seed()

    def step(self, action):
        current_action = action
        
        self.curr_episode += 1

        if self.curr_episode == MAX_TIMESTEP:

          print("Episode completed")
          # self.action_episode_memory += 1
          print("Action Count")

        self.current_action = action
        logging.basicConfig()
        self.x, self.v = run(action)
        print("Current Action: ", self.current_action)
        print("Current Location: ", self.x, ", ", self.v)

        self.state = (self.x, self.v)
        # reward = self.x
        # if(self.x == 0.5):
        #     reward = 25
        reward =-1
        done = bool(self.x >= self.goal_position and self.v >= self.goal_velocity)
        # return np.array(self.state), reward, self.curr_episode , {}
        return np.array(self.state), reward, done , {}

    def reset(self):
        self.curr_episode = 0
        self.action_episode_memory.append([])
        return np.array([0,0])

    # def _render(self, mode='human', close=False):
    #     return None 

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
    return x, v