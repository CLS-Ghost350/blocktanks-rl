import math, random

from .Bullet import Bullet
from .Target import Target
from .Map import Map
from .Player import Player

from .constants import Colors

import os

import sys

import pygame
pygame.init()

bg = pygame.image.load("grid.png")

class BlocktanksGame:
    FPS = 10 # used if render is enabled

    WINDOW_SIZE = (316*5, 165*5)

    BULLET_SPAWN_SPEED = 10 #100#30#15#10

    TARGET_SPAWN_SPEED = 30 #1

    PLAYER_BULLET_SPAWN_SPEED = 0

    def __init__(self, **kwargs): 
        self.doRender = kwargs.get("render", False)
        self._seed = kwargs.get("seed", 69)

        pygame.display.set_caption("Game View")

        if self.doRender:
            self.clock = pygame.time.Clock()
            self.window_surface = pygame.display.set_mode(BlocktanksGame.WINDOW_SIZE)
        else:
            self.window_surface = pygame.Surface(BlocktanksGame.WINDOW_SIZE)

        self.background = pygame.Surface(BlocktanksGame.WINDOW_SIZE)
        self.background.fill(pygame.Color('#ffffff'))
        #self.background.fill(pygame.Color('#000000'))

        self.map = Map.fromFile(os.path.join(os.path.dirname(__file__), "map.map"))

    def reset(self, seed=None):
        random.seed(seed or self._seed)

        self.timeSteps = 0

        self.player = Player(self.map)

        self.bullets = []
        self.spawnBulletCooldown = 5
        self.playerBulletCooldown = 5

        self.targets = []
        self.spawnTargetCooldown = 5

    def step(self, inputs):

        if self.doRender:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            pygame.display.flip()
            self.clock.tick(10)

        self.timeSteps += 1

        self.player.update(inputs)

        for bullet in self.bullets:
            bullet.update()

        self.bullets = [ bullet for bullet in self.bullets if bullet.despawnTime > 0 ]
        self.player_bullets = [bullet for bullet in self.bullets if bullet.team == "blue"]

        self.spawnBulletCooldown -= 1
        if self.spawnBulletCooldown < 0:
            self.spawnBulletCooldown = BlocktanksGame.BULLET_SPAWN_SPEED - round(min(self.timeSteps/1000, 1) * 7)

            self.bullets.append(Bullet.spawnRandomBullet((self.player.x, self.player.y), 200, 250, math.pi/4, "red", self.map))

        for target in self.targets:
            target.update()

        # Target Spawning
        self.spawnTargetCooldown -= 1
        if self.spawnTargetCooldown < 0:
            self.spawnTargetCooldown = BlocktanksGame.TARGET_SPAWN_SPEED
            
            self.targets.append(Target.spawnRandomTarget((self.player.x, self.player.y), 200, 250, self.map))

        # I'm trying this code out -> Spawns Target if none exist
        if not self.targets:
            self.targets.append(Target.spawnRandomTarget((self.player.x, self.player.y), 200, 250, self.map))

        # Adding Player Bullets
        self.playerBulletCooldown -= 1
        if (self.playerBulletCooldown < 0 and len(self.player_bullets) < 5):
            self.playerBulletCooldown = BlocktanksGame.PLAYER_BULLET_SPAWN_SPEED

            if self.player.isShooting == 1:
                #print(self.player.angle)
                self.bullets.append(Bullet(self.player.x, self.player.y, inputs["angle"], "blue", self.map))

        cameraPos = (self.player.x - BlocktanksGame.WINDOW_SIZE[0]/2, self.player.y - BlocktanksGame.WINDOW_SIZE[1]/2)

        self.window_surface.blit(self.background, (0, 0))
        #self.window_surface.blit(bg, (-500 - cameraPos[0], -500 - cameraPos[1]))

        self.map.draw(self.window_surface, cameraPos)

        self.player.draw(self.window_surface, cameraPos)

        for bullet in self.bullets:
            bullet.draw(self.window_surface, cameraPos)

        for target in self.targets:
            target.draw(self.window_surface, cameraPos)

        # Bullet Collision With Player
        colliding_player = False

        for bullet in self.bullets:
            if (bullet.team == "blue"): continue

            if circleRect(bullet.x, bullet.y, Bullet.RADIUS, 
                self.player.x - Player.SIZE/2, self.player.y - Player.SIZE/2,
                Player.SIZE, Player.SIZE):

                colliding_player = True
                break

            
        if colliding_player:
            return self.window_surface, { "DEATH" }
        
        # Collision With Targets
        colliding_target = False

        for bullet in self.player_bullets:
            for target in self.targets:
                if circleRect(bullet.x, bullet.y, Bullet.RADIUS, 
                    target.x - Player.SIZE/2, target.y - Player.SIZE/2, 
                    Player.SIZE, Player.SIZE):

                    self.targets.remove(target)
                    colliding_target = True
                    break
            else: # Stackoverflow Code for breaking out of Outer Loop
                continue
            break


        if colliding_target:
            return self.window_surface, {"KILL"}

        return self.window_surface, { }

    def render(self):
        pass

def circleRect(cx:float, cy:float, radius:float, rx:float, ry:float, rw:float, rh:float):

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


