from gymnasium import Env
from gymnasium.spaces import MultiDiscrete, Discrete, Box, Dict
import gymnasium as gym
import numpy as np
import math, random

import pygame

from collections import deque

from SimpleEnv.BlocktanksGame import BlocktanksGame

import cv2

class BlocktanksEnv(Env):
    DEATH_PENALTY = -30
    ALIVE_REWARD = 0
    KILL_REWARD = 20
    SHOOTING_PENALTY = -1
    WEAPON_PICKUP_REWARD = 1

    MAX_REWARD = max(max(-DEATH_PENALTY, -(SHOOTING_PENALTY)), ALIVE_REWARD + KILL_REWARD )

    instances = 0

    def __init__(self, **kwargs): 
        BlocktanksEnv.instances += 1
        print(BlocktanksEnv.instances)

        self.action_space = Dict({ "keys": MultiDiscrete([3, 3, 2]), "angle": Box(-1, 1, (1,), np.float32) })
        self.observation_space = Box(0, 255, (165, 316, 3), np.uint8)

        #self.n_steps = kwargs.get("n_steps", None)

        self.game = BlocktanksGame(**kwargs)

        self.render = kwargs.get("render")

    def render(self):
        pass

    def reset(self, *, seed=None, options=None) :
        self.game.reset(seed=seed)

        self.obs_frames = deque([ np.zeros((316, 165)), np.zeros((316, 165)), np.zeros((316, 165)) ], maxlen=3)
        #self.obs_frames = deque([ np.zeros(BlocktanksEnv.WINDOW_SIZE), np.zeros(BlocktanksEnv.WINDOW_SIZE), np.zeros(BlocktanksEnv.WINDOW_SIZE) ], maxlen=3)
        self.past_positions = deque([(0,0), (0,0), (0,0)], maxlen=3)

        return self.get_obs(), {}

    def step(self, action: Dict):
        inputs = { "keys": action["keys"], "angle": action["angle"] * math.pi }

        surface, events = self.game.step(inputs)

        imageData = BlocktanksEnv.get_obs_frame(surface)
        self.obs_frames.append(imageData)
        self.past_positions.append((self.game.player.x, self.game.player.y))
        curObs = self.get_obs()

        if self.render:
            cv2.imshow("AI View", curObs)

        # Reward Handling
        if "DEATH" in events:
            return curObs, BlocktanksEnv.DEATH_PENALTY / BlocktanksEnv.MAX_REWARD, True, False, {}

        reward = BlocktanksEnv.ALIVE_REWARD

        if "KILL" in events:
            reward += BlocktanksEnv.KILL_REWARD
        
        if "SHOOTING" in events:
            reward += BlocktanksEnv.SHOOTING_PENALTY

        if "WEAPON" in events:
            reward += BlocktanksEnv.WEAPON_PICKUP_REWARD

        return curObs, reward / BlocktanksEnv.MAX_REWARD, False, False, {}

    @staticmethod
    def get_obs_frame(surface: pygame.Surface): # no way of knowing past actions, which skew past frames
        img_data = pygame.surfarray.array3d(surface)

        # 5x downscale
        img_data = img_data[::5, ::5]

        # to grayscale
        img_data = np.dot(img_data[...,:3], [0.299, 0.587, 0.114])

        return img_data

    def get_obs(self):
        curPos = self.past_positions[len(self.past_positions) - 1]
        adjustedFrames = []

        for obs, pos in zip(list(self.obs_frames)[:-1], list(self.past_positions)[:-1]):
            dx = round((pos[0] - curPos[0]) / 5)
            dy = round((pos[1] - curPos[1]) / 5)

            adjustedObs = np.roll(obs, (dx, dy), (0, 1))
            if dx > 0:   adjustedObs[:dx, :] = 0#255
            elif dx < 0: adjustedObs[dx:, :] = 0#255

            if dy > 0:   adjustedObs[:, :dy] = 0#255
            elif dy < 0: adjustedObs[:, dy:] = 0#255

            adjustedFrames.append(adjustedObs)

        adjustedFrames.append(self.obs_frames[-1])

        img_data = np.asarray(adjustedFrames, dtype=np.uint8).swapaxes(0,2)#.swapaxes(0,1)
        #img_data = np.asarray(self.obs_frames, dtype=np.uint8).swapaxes(0,2)#.swapaxes(0,1)
       
        return img_data

        #return np.asarray([np.ones((316, 165))*0,np.ones((316, 165))*0,np.ones((316, 165))*255]).swapaxes(0,2)