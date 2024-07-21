import pygame, math

from .Map import Map
from .Bullet import Bullet

from .constants import Colors

class Player:
    SIZE = 50
    ARM_SIZE = 80
    SPEED = 8#4
    ORIGINAL_ARM_IMAGE = pygame.transform.scale(pygame.image.load('./SimpleEnv/Resources/arm.png'), (ARM_SIZE, ARM_SIZE))

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
        self.arm_image = pygame.transform.rotate(Player.ORIGINAL_ARM_IMAGE, math.degrees(-self.angle) - 90)

        #Calculation Crop
        image_size = self.arm_image.get_width()
        self.crop = ((image_size - Player.ARM_SIZE)/2, (image_size - Player.ARM_SIZE)/2, Player.ARM_SIZE, Player.ARM_SIZE)

    def draw(self, surface:pygame.Surface, cameraPos:tuple):
        pygame.draw.rect(surface, Colors.BLUE, pygame.Rect(
            self.x - cameraPos[0] - Player.SIZE/2, self.y - cameraPos[1] - Player.SIZE/2,
            Player.SIZE,
            Player.SIZE
        ))
        surface.blit(self.arm_image, (self.x - cameraPos[0] - Player.ARM_SIZE/2, self.y - cameraPos[1] - Player.ARM_SIZE/2), )