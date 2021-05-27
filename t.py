import numpy as np


class Tile:
    def __init__(self, x, y, terrain):
        self.row = x
        self.column = y
        self.terrain = terrain
        self.closed = 0
        self.open = 0
        self.g_score = 0
        self.h_score = 0
        self.f_score = 0
        self.prev = None
    def __str__(self):
        if self.prev == None:
            return "Tile:(%s,%s) %s cost:%s f_score:%s prev: None " % ( self.column, self.row, self.terrain, self.g_score, self.f_score)
        else:
            return "Tile:(%s,%s) %s cost:%s f_score:%s prev: (%s,%s) " % (self.column, self.row, self.terrain, self.g_score, self.f_score, self.prev.row, self.prev.column)

    def __lt__(self, other):
        return self.f_score < other.f_score

    def is_same(self, other):
        return self.row == other.row and self.column == other.column


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
