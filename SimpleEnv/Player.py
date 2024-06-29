import pygame

from .Map import Map

class Player:
    RED = (232,50,41)
    FADED_RED = (234,140,139)
    BLUE = (66, 85, 210)
    FADED_BLUE = (160, 168, 199)

    SIZE = 50
    SPEED = 8#4

    def __init__(self, map:Map):
        self.map = map
        self.x = 1050
        self.y = 1050

    def update(self, inputs):
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

    def draw(self, surface:pygame.Surface, cameraPos:tuple):
        pygame.draw.rect(surface, Player.BLUE, pygame.Rect(
            self.x - cameraPos[0] - Player.SIZE/2, self.y - cameraPos[1] - Player.SIZE/2,
            Player.SIZE,
            Player.SIZE
        ))