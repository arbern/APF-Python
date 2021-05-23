import numpy as np
from PIL import Image
"""
10 = Water Tile
4 = Forest Tile
3 = Dirt Tile
7 = Mountain lvl 1 Tile
8 = Mountain lvl 2 Tile
5 = Desert Tile
11 = Lava Tile
2 = Plains Tile
9 = Snow Mountain Tile
1 = Road Tile
6 = Snow Tile
0 = Capitol tile
12 = Ice Tile
13 = Ice lvl 2 Tile 

This is the legend 
"""

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



array_of_tiles = np.empty((0,350), dtype=np.int32)

with open('agoniaMap2.txt') as f:
    for line in f:
        array_of_tiles = np.vstack((array_of_tiles, np.array(list(map(int, line.split())))))


simple_map = [BLACK, YELLOW, GREEN, BROWN, DARK_GREEN, LIGHT_YELLOW, WHITE, DARK_GREY, GREY, WHITE, BLUE, RED, LIGHT_BLUE, ICE_BLUE]

rgb_arr = np.zeros((array_of_tiles.shape[1], array_of_tiles.shape[0], 3))

for j, row in enumerate(array_of_tiles):
    for i, col in enumerate(row):
        rgb_arr[j][i][0] = simple_map[col][0]
        rgb_arr[j][i][1] = simple_map[col][1]
        rgb_arr[j][i][2] = simple_map[col][2]
        
img = Image.fromarray(np.uint8(rgb_arr), 'RGB')
img.show()
