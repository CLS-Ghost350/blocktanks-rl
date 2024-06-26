from gym import Env
from gym.spaces import MultiDiscrete, Box, Dict
import numpy as np
import math, random

from .Bullet import Bullet
from .Target import Target
from .Map import Map
from .Player import Player

from collections import deque

import os

import sys

import cv2

import pygame
pygame.init()

bg = pygame.image.load("grid.png")

class BlocktanksEnv(Env):
    FPS = 10

    RED = (232,50,41)
    FADED_RED = (234,140,139)
    BLUE = (66, 85, 210)
    FADED_BLUE = (160, 168, 199)
    WALL_GREY = (180,180,180)
    
    AD_BORDER_BLACK = (0, 0, 0)
    RESPAWN_GREY = (221, 221, 221)
    COUNTDOWN_GREY = (68, 68, 68)
    KILL_RED = (255, 26, 0)
    DEATH_BLUE = (56, 0, 255)

    DEATH_PENALTY = 0#600
    ALIVE_REWARD = 1

    WINDOW_SIZE = (316*5, 165*5)

    BULLET_SPAWN_SPEED = 10#30#15#10

    TARGET_SPAWN_SPEED = 1

    instances = 0

    def __init__(self, **kwargs): 
        BlocktanksEnv.instances += 1
        print(BlocktanksEnv.instances)
        
        self.action_space = Dict({ "keys": MultiDiscrete([3, 3]), "angle": Box(0, 255, (1), np.uint8) })
        self.observation_space = Box(0, 255, (165, 316, 3), np.uint8)

        #self.n_steps = kwargs.get("n_steps", None)

        self.doRender = kwargs.get("render", False)
        self._seed = kwargs.get("seed", 69)

        pygame.display.set_caption("Game View")

        if self.doRender:
            self.clock = pygame.time.Clock()
            self.window_surface = pygame.display.set_mode(BlocktanksEnv.WINDOW_SIZE)
        else:
            self.window_surface = pygame.Surface(BlocktanksEnv.WINDOW_SIZE)

        self.background = pygame.Surface(BlocktanksEnv.WINDOW_SIZE)
        self.background.fill(pygame.Color('#ffffff'))
        #self.background.fill(pygame.Color('#000000'))

        self.map = Map.fromFile(os.path.join(os.path.dirname(__file__), "map.map"))

    def reset(self):
        random.seed(self._seed)

        self.timeSteps = 0

        self.player = Player(self.map)

        self.bullets = []
        self.spawnBulletCooldown = 5

        self.targets = []
        self.spawnTargetCooldown = 5

        self.obs_frames = deque([ np.zeros((316, 165)), np.zeros((316, 165)), np.zeros((316, 165)) ], maxlen=3)
        #self.obs_frames = deque([ np.zeros(BlocktanksEnv.WINDOW_SIZE), np.zeros(BlocktanksEnv.WINDOW_SIZE), np.zeros(BlocktanksEnv.WINDOW_SIZE) ], maxlen=3)
        self.past_positions = deque([(0,0), (0,0), (0,0)], maxlen=3)

        return self.get_obs()

    def step(self, action):
        if self.doRender:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            pygame.display.flip()
            
            cv2.imshow("AI View", self.get_obs())
            self.clock.tick(10)

        self.timeSteps += 1

        self.player.update(action)
    

        for bullet in self.bullets:
            bullet.update()

        self.bullets = [ bullet for bullet in self.bullets if bullet.despawnTime > 0 ]

        self.spawnBulletCooldown -= 1
        if self.spawnBulletCooldown < 0:
            self.spawnBulletCooldown = BlocktanksEnv.BULLET_SPAWN_SPEED - round(min(self.timeSteps/1000, 1) * 7)

            self.bullets.append(Bullet.spawnRandomBullet((self.player.x, self.player.y), 200, 250, math.pi/4, "red", self.map))


        for target in self.targets:
            target.update()

        self.spawnTargetCooldown -= 1
        if self.spawnTargetCooldown < 0:
            self.spawnTargetCooldown = BlocktanksEnv.TARGET_SPAWN_SPEED
            
            self.targets.append(Target.spawnRandomTarget((self.player.x, self.player.y), 200, 250, self.map))



        cameraPos = (self.player.x - BlocktanksEnv.WINDOW_SIZE[0]/2, self.player.y - BlocktanksEnv.WINDOW_SIZE[1]/2)

        self.window_surface.blit(self.background, (0, 0))
        #self.window_surface.blit(bg, (-500 - cameraPos[0], -500 - cameraPos[1]))

        self.map.draw(self.window_surface, cameraPos)

        self.player.draw(self.window_surface, cameraPos)

        for bullet in self.bullets:
            bullet.draw(self.window_surface, cameraPos)

        for target in self.targets:
            target.draw(self.window_surface, cameraPos)


        colliding = False

        for bullet in self.bullets:

            if circleRect(bullet.x, bullet.y, Bullet.RADIUS, 
                self.player.x - Player.SIZE/2, self.player.y - Player.SIZE/2,
                Player.SIZE, Player.SIZE):

                colliding = True
                break

        imageData = self.get_obs_frame()
        self.obs_frames.append(imageData)
        self.past_positions.append((self.player.x, self.player.y))
        curObs = self.get_obs()
            
        if colliding:
            return curObs, -BlocktanksEnv.DEATH_PENALTY, True, {} 

        return curObs, BlocktanksEnv.ALIVE_REWARD, False, {}

    def render(self):
        pass
        #print(f"{self.x} {self.y} {self.x - abs(self.y)}")
        #self.clock.tick(10)

    def get_obs_frame(self): # no way of knowing past actions, which skew past frames
        img_data = pygame.surfarray.array3d(self.window_surface)

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

def circleRect(cx, cy, radius, rx, ry, rw, rh):

  # temporary variables to set edges for testing
  testX = cx
  testY = cy

  # which edge is closest?
  if cx < rx:      testX = rx;      # test left edge
  elif cx > rx+rw: testX = rx+rw;   # right edge
  if cy < ry:      testY = ry;      # top edge
  elif cy > ry+rh: testY = ry+rh;   # bottom edge

  # get distance from closest edges
  distX = cx-testX
  distY = cy-testY
  distance = math.sqrt( (distX*distX) + (distY*distY) )

  # if the distance is less than the radius, collision!
  if (distance <= radius):
    return True
  
  return False


