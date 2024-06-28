import pygame

class Map:
    TILE_SIZE = 100
    COLOR = (180,180,180)

    @classmethod
    def fromFile(cls, filepath:str):
        with open(filepath, "r") as f:
            tiles = [ list(line) for line in f.readlines() ]

        return cls(tiles)

    def __init__(self, tiles:list): 
        self.tiles = tiles

    def update(self):
        pass

    def getTileRect(self, r, c):
        return pygame.Rect(c*Map.TILE_SIZE, r*Map.TILE_SIZE, Map.TILE_SIZE, Map.TILE_SIZE)
    
    def draw(self, surface, cameraPos):
    
        for r, row in enumerate(self.tiles):
            for c, tile in enumerate(row):

                if tile == "w":
                    pygame.draw.rect(surface, Map.COLOR, 
                        (c*Map.TILE_SIZE - cameraPos[0], r*Map.TILE_SIZE - cameraPos[1], Map.TILE_SIZE, Map.TILE_SIZE))