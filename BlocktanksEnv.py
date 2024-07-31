from gymnasium import Env
from gymnasium.spaces import MultiDiscrete, Discrete, Box
import gymnasium as gym
import numpy as np
import math, random

import pygame

from collections import deque

from SimpleEnv.BlocktanksGame import BlocktanksGame

import cv2

class BlocktanksEnv(Env):
    ANGLES = 24
    FRAMES_STACKED = 4 # either 3 (RGB) or 4 (RGBA); order from oldest to newest: BGRA

    ALIVE_REWARD = 0
    KILL_REWARD = 1
    WEAPON_PICKUP_REWARD = 0.5

    DEATH_PENALTY = -2
    SHOOTING_PENALTY = -0.02

    #MAX_SHOOTING_SHAPED_REWARD = 1000
    #MAX_DODGING_SHAPED_REWARD = 0#350

    #MAX_REWARD = max(-(DEATH_PENALTY + SHOOTING_PENALTY), ALIVE_REWARD + KILL_REWARD + WEAPON_PICKUP_REWARD)

    EPISODE_STEPS_LIMIT = 256

    instances = 0

    def __init__(self, **kwargs): 
        BlocktanksEnv.instances += 1
        print(BlocktanksEnv.instances)

        self.action_space = MultiDiscrete([3, 3, 2, BlocktanksEnv.ANGLES]) # x-move, y-move, shoot (TODO: add powerups to this), angle
        self.observation_space = Box(0, 255, (165, 316, 4), np.uint8)

        #self.n_steps = kwargs.get("n_steps", None)

        self.game = BlocktanksGame(**kwargs)

        self.render = kwargs.get("render")

    def render(self):
        pass

    def reset(self, *, seed=None, options=None) :
        #print("reset")

        self.game.reset(seed=seed)

        self.obs_frames = deque([ np.zeros((316, 165)) for i in range(BlocktanksEnv.FRAMES_STACKED) ], maxlen=BlocktanksEnv.FRAMES_STACKED)
        #self.obs_frames = deque([ np.zeros(BlocktanksEnv.WINDOW_SIZE), np.zeros(BlocktanksEnv.WINDOW_SIZE), np.zeros(BlocktanksEnv.WINDOW_SIZE) ], maxlen=3)
        self.past_positions = deque([(0,0) for i in range(BlocktanksEnv.FRAMES_STACKED) ], maxlen=BlocktanksEnv.FRAMES_STACKED)

        self.episode_steps = 0

        return self.get_obs(), {}

    def step(self, action: MultiDiscrete):
        #print("step")

        self.episode_steps += 1

        inputs = { "keys": action[0:3], "angle": action[3] / BlocktanksEnv.ANGLES * 2*math.pi }

        (surface, events, shooting_distance, dodging_distance) = self.game.step(inputs)

        imageData = BlocktanksEnv.get_obs_frame(surface)
        self.obs_frames.append(imageData)
        self.past_positions.append((self.game.player.x, self.game.player.y))
        curObs = self.get_obs()

        if self.render:
            cv2.imshow("AI View", curObs)
            #cv2.imwrite("obs.png", curObs)

        # Reward Handling
        reward = BlocktanksEnv.ALIVE_REWARD
        terminated = False
        truncated = False

        if "DEATH" in events:
            reward += BlocktanksEnv.DEATH_PENALTY
            terminated = True

        if "KILL" in events:
            reward += BlocktanksEnv.KILL_REWARD
        
        if "SHOOTING" in events:
            reward += BlocktanksEnv.SHOOTING_PENALTY

        if "WEAPON" in events:
            reward += BlocktanksEnv.WEAPON_PICKUP_REWARD

        # Shaped Reward Handling
        # Shooting Shaped Rewards
        #if (shooting_distance):
        #    shooting_shaped_reward = max(0, 1000 - min(shooting_distance[0])) / 10000 #I'm not sure what's a good value to give
        #    reward += shooting_shaped_reward
        #    #print("SHOOTING SHAPED REWARD", shooting_shaped_reward)

        #if (dodging_distance):
        #    sorted(dodging_distance)
        #    dodging_shaped_reward = max(B, dodging_distance[0]) / 3500
        #    reward += dodging_shaped_reward
        #    #print("DODGING SHAPED REWARD", dodging_shaped_reward)

        truncated = self.episode_steps >= BlocktanksEnv.EPISODE_STEPS_LIMIT

        #return curObs, reward / BlocktanksEnv.MAX_REWARD, terminated, truncated, {}
        return curObs, reward, terminated, truncated, {}

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