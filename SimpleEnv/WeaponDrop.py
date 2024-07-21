import math, random, pygame

from .Map import Map
from .constants import Colors

class WeaponDrop:
    TYPES = ["bomb", "bottle_bomb", "flashbang", "hand_grenade", "rapid_bullet", "rocket", "shotgun_shell", "sniper_bullet"]
    SIZE = 40

    @classmethod
    def spawnRandomWeaponDrop(cls, map:Map):
        validSpawn = False

        row = -1
        col = -1


        while (not validSpawn):       
            # Pick a random tile
            row = random.randint(0, len(map.tiles)-1)
            col = random.randint(0, len(map.tiles[row])-1)

            #print("lengths", len(map.tiles), len(map.tiles[row]), row, col)
            if map.tiles[row][col] == 'a':
                validSpawn = True
                break
        
        return cls(map, map.TILE_SIZE * col + map.TILE_SIZE/2, map.TILE_SIZE * row + map.TILE_SIZE/2)

    def __init__(self, map:Map, x:float, y:float): 
        self.x = x
        self.y = y

        self.type = random.choice(self.TYPES)
        self.image = pygame.transform.scale(pygame.image.load('./SimpleEnv/Resources/'+ self.type + '.png'), (self.SIZE, self.SIZE))
        
        #Hitbox rect
        
        self.map = map
        

    def update(self):
        # Do we need to add a despawn feature?
        pass
    
    def draw(self, surface, cameraPos):
        # pygame.draw.rect(surface, Colors.TESTING_GREEN, pygame.Rect(
        #     self.x - cameraPos[0] - self.SIZE/2, self.y - cameraPos[1] - WeaponDrop.SIZE/2,
        #     WeaponDrop.SIZE,
        #     WeaponDrop.SIZE
        # ))
        surface.blit(self.image, (self.x - cameraPos[0] - WeaponDrop.SIZE/2, self.y - cameraPos[1] - WeaponDrop.SIZE/2))