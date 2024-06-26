import random, math
import pygame

from .Player import Player
from .Map import Map

class Target(Player):

    @classmethod
    def spawnRandomTarget(cls, playerPos, minDist, maxDist, map): 
        colliding = True
        i = 0

        while colliding and i < 20:
            i += 1

            dist = random.uniform(minDist, maxDist)
            angle = random.uniform(-math.pi, math.pi)

            x = math.cos(angle) * dist + playerPos[0]
            y = math.sin(angle) * dist + playerPos[1]

            left = x - Player.SIZE/2
            top = y - Player.SIZE/2

            colliding = False

            tileTR = int(top // Map.TILE_SIZE)
            tileLC = int(left // Map.TILE_SIZE)
    
            for r in range(tileTR, tileTR + 2): 
                for c in range(tileLC, tileLC + 2):
                    if map.tiles[r][c] == "w":
                        if pygame.Rect.colliderect(map.getTileRect(r, c), pygame.Rect(left, top, Player.SIZE, Player.SIZE)):
                            colliding =True
                            print("coll", map.getTileRect(r, c))
                            break

        return cls(map, x, y)

    def __init__(self, map, x, y):
        self.map = map
        self.x = x
        self.y = y

    def update(self):
        pass

    def draw(self, surface, cameraPos):
        pygame.draw.rect(surface, Player.RED, pygame.Rect(
            self.x - cameraPos[0] - Player.SIZE/2, self.y - cameraPos[1] - Player.SIZE/2,
            Player.SIZE,
            Player.SIZE
        ))