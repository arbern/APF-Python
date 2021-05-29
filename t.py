import numpy as np

BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BROWN = (138, 71, 0)
DARK_GREEN = (2, 81, 0)
LIGHT_YELLOW = (255, 255, 157)
WHITE = (255, 255, 255)
DARK_GREY = (105,105,105)
GREY = (192,192,192)
BLUE = (0, 102, 204)
RED = (204, 0, 0)
LIGHT_BLUE = (0, 204, 204)
ICE_BLUE = (51, 255, 255)
simple_map = [BLACK, YELLOW, GREEN, BROWN, DARK_GREEN, LIGHT_YELLOW, WHITE, DARK_GREY, GREY, WHITE, BLUE, RED, LIGHT_BLUE, ICE_BLUE]

class Tile:
    def __init__(self, x, y, terrain):
        self.row = x
        self.column = y
        self.terrain = terrain
        self.is_on_path = 0
        self.closed = 0
        self.open = 0
        self.g_score = 0
        self.h_score = 0
        self.f_score = 0
        self.prev = None
    def __str__(self):
        if self.prev == None:
            return "Tile:(%s,%s) %s cost:%s f_score:%s prev: None " % ( self.column +1, self.row +1, self.terrain, self.g_score, self.f_score)
        else:
            return "Tile:(%s,%s) %s cost:%s f_score:%s prev: (%s,%s)step cost:%s " % (self.column +1, self.row +1, self.terrain, self.g_score, self.f_score, self.prev.column +1, self.prev.row +1, self.g_score-self.prev.g_score)

    def __lt__(self, other):
        return self.f_score < other.f_score

    def is_same(self, other):
        return self.row == other.row and self.column == other.column

    def to_img(self):
        row_size = 7
        col_size =7
        colour_size =3
        tile_img = np.zeros((row_size, col_size, 3))
        for i in range(row_size):
            if i ==0 or i == 6:
                for j in range(col_size):
                    for z in range(colour_size):
                        tile_img [i][j][z] = simple_map[1][z]
            elif self.is_on_path == 1 and (i in range (2,5)):
                if i == 2 or i == 4:
                    for j in range(col_size):
                        if j == 0 or j == 6:
                            for z in range(3):
                                tile_img [i][j][z] = simple_map [1][z]
                        elif j==3:
                            for z in range(3):
                                tile_img [i][j][z] = simple_map [0][z]
                        else:
                            for z in range(3):
                                tile_img [i][j][z] = simple_map [self.terrain][z]
                elif i == 3:
                    for j in range(col_size):
                        if j == 0 or j == 6:
                            for z in range(3):
                                tile_img [i][j][z] = simple_map [1][z]
                        elif j==2 or j==3 or j==4:
                            for z in range(3):
                                tile_img [i][j][z] = simple_map [0][z]
                        else:
                            for z in range(3):
                                tile_img [i][j][z] = simple_map [self.terrain][z]
            else:
                for j in range(col_size):
                    if j ==0 or j == 6:
                        for z in range(3):
                            tile_img [i][j][z] = simple_map [1][z]
                    else:
                        for z in range(3):
                           tile_img [i][j][z] = simple_map [self.terrain][z]

        return tile_img

class Map:
    def __init__(self):
        array_of_tiles = np.empty((0,350), dtype=np.int32)
        with open('map.txt') as f:
            for line in f:
                array_of_tiles = np.vstack((array_of_tiles, np.array(list(map(int, line.split())))))
        self.raw_map = array_of_tiles
        rows = 350
        columns = 350
        self.map_of_tiles = np.empty((350,350), dtype=Tile)
        for i in range(rows):
            for j in range(columns):
                self.map_of_tiles[i,j] = Tile(i,j,self.raw_map[i,j])

class MvpMod:
    def __init__(self, tribe, item, overloaded):
        self.tribe = tribe
        self.item = item
        self.overloaded = overloaded
