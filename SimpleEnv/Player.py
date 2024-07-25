import pygame, math, random

from .Utils import Utils
from .Map import Map
from .Bullet import Bullet

from .constants import Colors

class Player:
    SIZE = 50
    ARM_SIZE = 80
    SPEED = 8#4
    ORIGINAL_ARM_IMAGE = pygame.transform.scale(pygame.image.load('./SimpleEnv/Resources/arm.png'), (ARM_SIZE, ARM_SIZE))

    @staticmethod
    def get_random_spawn(boundLeft, boundTop, boundRight, boundBottom, map:Map): 
        colliding = True
        i = 0

        while colliding and i < 20:
            i += 1

            x = random.uniform(boundLeft, boundRight)
            y = random.uniform(boundTop, boundBottom)


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
        return (1050, 1050) if colliding else (x, y)

    def __init__(self, map:Map):
        self.map = map
        self.arm_image = Player.ORIGINAL_ARM_IMAGE
        self.x = 1050
        self.y = 1050
        self.crop = ()

    def update(self, inputs):
        # Movement
        moveY = inputs["keys"][0]
        moveX = inputs["keys"][1]

        dx = 0
        dy = 0
        
        if moveY == 0: #S
            dy += Player.SPEED
        elif moveY == 2: # W
            dy -= Player.SPEED

        if moveX == 0: # A
            dx -= Player.SPEED
        elif moveX == 2: # D
            dx += Player.SPEED

        self.y += dy
    
        left = int((self.x - Player.SIZE/2) // Map.TILE_SIZE)
        right = int((self.x + Player.SIZE/2 - 1) // Map.TILE_SIZE)
        
        if dy > 0:
            bottom = int((self.y + Player.SIZE/2) // Map.TILE_SIZE)
            
            if self.map.tiles[bottom][left] == "w" or self.map.tiles[bottom][right] == "w":
                self.y = bottom * Map.TILE_SIZE - Player.SIZE/2
                
        elif dy < 0:
            top = int((self.y - Player.SIZE/2) // Map.TILE_SIZE)
            
            if self.map.tiles[top][left] == "w" or self.map.tiles[top][right] == "w":
                self.y = (top+1) * Map.TILE_SIZE + Player.SIZE/2
        
        self.x += dx
        
        bottom = int((self.y + Player.SIZE/2 - 1) // Map.TILE_SIZE)
        top = int((self.y - Player.SIZE/2) // Map.TILE_SIZE)
        
        if dx > 0:
            right = int((self.x + Player.SIZE/2) // Map.TILE_SIZE)
            
            if self.map.tiles[top][right] == "w" or self.map.tiles[bottom][right] == "w":
                self.x = right * Map.TILE_SIZE - Player.SIZE/2
                
        elif dx < 0:
            left = int((self.x - Player.SIZE/2) // Map.TILE_SIZE)
            
            if self.map.tiles[top][left] == "w" or self.map.tiles[bottom][left] == "w":
                self.x = (left+1) * Map.TILE_SIZE + Player.SIZE/2

        # Shooting
        self.isShooting = inputs["keys"][2]
        self.angle = inputs["angle"]

        # Updating Arm Angle
        self.arm_image = Utils.rotate_center(Player.ORIGINAL_ARM_IMAGE, math.degrees(-self.angle) - 90, self.x, self.y)

    def draw(self, surface:pygame.Surface, cameraPos:tuple):
        pygame.draw.rect(surface, Colors.BLUE, pygame.Rect(
            self.x - cameraPos[0] - Player.SIZE/2, self.y - cameraPos[1] - Player.SIZE/2,
            Player.SIZE,
            Player.SIZE
        ))
        # Blitting with camera offset
        surface.blit(self.arm_image[0], self.arm_image[1].move(-cameraPos[0], -cameraPos[1]))