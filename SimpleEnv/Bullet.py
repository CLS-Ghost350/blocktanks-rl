import math, random, pygame

from .Map import Map
from .constants import Colors

class Bullet:
    RADIUS = 7
    HITBOX_SIZE = 11
    SPEED = 64#8

    @classmethod
    def spawnRandomBullet(cls, playerPos:tuple, minDist:float, maxDist:float, angleDeviation:float, team:str, map:Map):
        dist = random.uniform(minDist, maxDist)
        angle = random.uniform(-math.pi, math.pi)

        x = math.cos(angle) * dist + playerPos[0]
        y = math.sin(angle) * dist + playerPos[1]

        direction = random.uniform(-angleDeviation, angleDeviation) + angle + math.pi

        return cls(x, y, direction, team, map)

    @classmethod
    def spawnTargettedBullet(cls, playerPos:tuple, playerVel:float, minDist:float, maxDist:float, team:str, map:Map):
        dist = random.uniform(minDist, maxDist)
        angle = random.uniform(-math.pi, math.pi)

        impactTime = dist / Bullet.SPEED

        x = math.cos(angle)*dist + playerPos[0] + playerVel[0]*impactTime
        y = math.sin(angle)*dist + playerPos[1] + playerVel[1]*impactTime

        direction = angle + math.pi

        return cls(x, y, direction, team, map)

    def __init__(self, x, y, direction, team, map): 
        self.x = x
        self.y = y
        self.direction = direction

        self.team = team
        
        self.map = map

        self.dx = math.cos(self.direction) * Bullet.SPEED
        self.dy = math.sin(self.direction) * Bullet.SPEED

        self.bounces = 1

        self.despawnTime = 300

    def update(self):
        self.despawnTime -= 1

        self.y += self.dy

        left = int((self.x - Bullet.HITBOX_SIZE/2) // Map.TILE_SIZE)
        right = int((self.x + Bullet.HITBOX_SIZE/2 - 1) // Map.TILE_SIZE)
        
        if self.dy > 0:
            bottom = int((self.y + Bullet.HITBOX_SIZE/2) // Map.TILE_SIZE)
            
            if self.map.tiles[bottom][left] == "w" or self.map.tiles[bottom][right] == "w":
                wallY = bottom * Map.TILE_SIZE - Bullet.HITBOX_SIZE/2
                self.y = wallY - (self.y - wallY)

                self.dy *= -1
                self.bounces -= 1

                if self.bounces < 0:
                    self.despawnTime = -1
                    return
                
        elif self.dy < 0:
            top = int((self.y - Bullet.HITBOX_SIZE/2) // Map.TILE_SIZE)
            
            if self.map.tiles[top][left] == "w" or self.map.tiles[top][right] == "w":
                wallY = (top+1) * Map.TILE_SIZE + Bullet.HITBOX_SIZE/2
                self.y = wallY + (wallY - self.y)

                self.dy *= -1
                self.bounces -= 1

                if self.bounces < 0:
                    self.despawnTime = -1
                    return
        
        self.x += self.dx
        
        bottom = int((self.y + Bullet.HITBOX_SIZE/2 - 1) // Map.TILE_SIZE)
        top = int((self.y - Bullet.HITBOX_SIZE/2) // Map.TILE_SIZE)
        
        if self.dx > 0:
            right = int((self.x + Bullet.HITBOX_SIZE/2) // Map.TILE_SIZE)
            
            if self.map.tiles[top][right] == "w" or self.map.tiles[bottom][right] == "w":
                wallX = right * Map.TILE_SIZE - Bullet.HITBOX_SIZE/2
                self.x = wallX - (self.x - wallX)

                self.dx *= -1
                self.bounces -= 1

                if self.bounces < 0:
                    self.despawnTime = -1
                    return
                
        elif self.dx < 0:
            left = int((self.x - Bullet.HITBOX_SIZE/2) // Map.TILE_SIZE)
            
            if self.map.tiles[top][left] == "w" or self.map.tiles[bottom][left] == "w":
                wallX = (left+1) * Map.TILE_SIZE + Bullet.HITBOX_SIZE/2
                self.x = wallX + (wallX - self.x)

                self.dx *= -1
                self.bounces -= 1

                if self.bounces < 0:
                    self.despawnTime = -1
                    return

        if self.x < 100 or self.y < 100 or self.x > 2000 or self.y > 2000: 
            self.despawnTime = -1
    
    def draw(self, surface, cameraPos):
        pygame.draw.circle(surface, Colors.BULLET[self.team], (self.x - cameraPos[0], self.y - cameraPos[1]), Bullet.RADIUS)