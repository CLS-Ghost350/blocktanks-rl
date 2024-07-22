import random, math
import pygame

from .Player import Player
from .Map import Map

from .constants import Colors

class Target(Player):

    SPEED = 8 
    MAX_MOVEMENT_COOLDOWN = 35

    @classmethod
    def spawnRandomTarget(cls, playerPos:tuple, minDist:float, maxDist:float, map:Map): 
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
                    if map.tiles[r][c] == "w" or map.tiles[r][c] == "o":
                        if pygame.Rect.colliderect(map.getTileRect(r, c), pygame.Rect(left, top, Player.SIZE, Player.SIZE)):
                            colliding =True
                            #print("coll", map.getTileRect(r, c))
                            break

        return cls(map, x, y)

    def __init__(self, map:Map, x:float, y:float):
        self.map = map
        self.x = x
        self.y = y

        self.dx = random.choice([-1, 0, 1]) * self.SPEED
        self.dy = random.choice([-1, 0, 1]) * self.SPEED

        self.move_cooldown = random.randint(1, self.MAX_MOVEMENT_COOLDOWN) #Cooldown for change of movement direction
    
    def changeDirection(self):
        self.dx = random.choice([-1, 0, 1]) * self.SPEED
        self.dy = random.choice([-1, 0, 1]) * self.SPEED

    def update(self):
        self.move_cooldown -= 1
        if (self.move_cooldown < 0):
            self.changeDirection()
            self.move_cooldown = random.randint(1, self.MAX_MOVEMENT_COOLDOWN)

        # Wall Collisions
        self.y += self.dy
        
        left = int((self.x - Player.SIZE/2) // Map.TILE_SIZE)
        right = int((self.x + Player.SIZE/2 - 1) // Map.TILE_SIZE)
        
        if self.dy > 0:
            bottom = int((self.y + Player.SIZE/2) // Map.TILE_SIZE)
            
            if self.map.tiles[bottom][left] == "w" or self.map.tiles[bottom][right] == "w":
                self.y = bottom * Map.TILE_SIZE - Player.SIZE/2
                
        elif self.dy < 0:
            top = int((self.y - Player.SIZE/2) // Map.TILE_SIZE)
            
            if self.map.tiles[top][left] == "w" or self.map.tiles[top][right] == "w":
                self.y = (top+1) * Map.TILE_SIZE + Player.SIZE/2
        
        self.x += self.dx
        
        bottom = int((self.y + Player.SIZE/2 - 1) // Map.TILE_SIZE)
        top = int((self.y - Player.SIZE/2) // Map.TILE_SIZE)
        
        if self.dx > 0:
            right = int((self.x + Player.SIZE/2) // Map.TILE_SIZE)
            
            if self.map.tiles[top][right] == "w" or self.map.tiles[bottom][right] == "w":
                self.x = right * Map.TILE_SIZE - Player.SIZE/2
                
        elif self.dx < 0:
            left = int((self.x - Player.SIZE/2) // Map.TILE_SIZE)
            
            if self.map.tiles[top][left] == "w" or self.map.tiles[bottom][left] == "w":
                self.x = (left+1) * Map.TILE_SIZE + Player.SIZE/2
            
    def draw(self, surface:pygame.Surface, cameraPos:tuple):
        pygame.draw.rect(surface, Colors.RED, pygame.Rect(
            self.x - cameraPos[0] - Player.SIZE/2, self.y - cameraPos[1] - Player.SIZE/2,
            Player.SIZE,
            Player.SIZE
        ))
        surface.blit(Player.ORIGINAL_ARM_IMAGE, (self.x - cameraPos[0] - Player.ARM_SIZE/2, self.y - cameraPos[1] - Player.ARM_SIZE/2))