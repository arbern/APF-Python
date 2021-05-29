import numpy as np
import heapq
import t
from PIL import Image

# Creating dictionary
# key will be tribe
# values will be array of mvp costs
# 0 = Capitol tile
# 1 = Road Tile
# 2 = Plains Tile
# 3 = Dirt Tile
# 4 = Forest Tile
# 5 = Desert Tile
# 6 = Snow Tile
# 7 = Mountain lvl 1 Tile
# 8 = Mountain lvl 2 Tile
# 9 = Snow Mountain Tile
# 10 = Water Tile
# 11 = Lava Tile
# 12 = Ice Tile
# 13 = Ice lvl 2 Tile
myDict = {}

# Adding list as value
myDict["kiith"] = [5, 13, 22, 19, 22, 18, 38, 46, 65, -1, -1, 200, -1, -1]

agoniasMap = t.Map()


def get_neigbours(current, agoniasMap):
    neighbours = []
    for i in range (current.row - 1, current.row + 2):
        if i > -1 and i < 350:
            for j in range (current.column - 1, current.column + 2):
                if j > -1 and j < 350:
                    candidate_for_neighbour = agoniasMap.map_of_tiles[i, j]
                    if not current.is_same(candidate_for_neighbour):
                        neighbours.append(agoniasMap.map_of_tiles[i, j])

    return neighbours


def get_straight_step_cost(terrain, mvp_mods):
    return myDict.get(mvp_mods.tribe)[terrain] # TODO other modifiers


def build_and_mark_path_to(e_tile):
    path=[]
    current_tile = e_tile
    current_tile.is_on_path=1
    path.append(current_tile)
    while current_tile.prev != None:
        current_tile=current_tile.prev
        current_tile.is_on_path=1
        path.append(current_tile)
    return path


def step_cost(current, neighbour, mvp_mods):
    straight_step_cost = get_straight_step_cost(neighbour.terrain, mvp_mods)
    if current.row==neighbour.row or current.column == neighbour.column: # stright step
        return straight_step_cost
    else:
        return int(1.414 * straight_step_cost)


def heuristic_estimate_of_distance_between(start, end):
    lowest_diagonal_step_cost = 5
    lowest_straight_step_cost = 3
    x_diff = abs(start.row - end.row)
    y_diff = abs(start.column - end.column)
    number_of_diagonal_steps = min(x_diff, y_diff)
    number_of_straight_steps = abs(x_diff-y_diff)
    return number_of_diagonal_steps * lowest_diagonal_step_cost + number_of_straight_steps * lowest_straight_step_cost


def find_path(s_tile, e_tile, agoniasMap, mvp_mods):
    print("A* start")
    # https://pl.wikipedia.org/wiki/Algorytm_A*#Algorytm_A*_w_pseudokodzie

    # open_set priority heap of tiles to be checked at start there is only start_tile
    open_set = []
    x = heuristic_estimate_of_distance_between(s_tile, e_tile)
    s_tile.h_score = heuristic_estimate_of_distance_between(s_tile, e_tile)
    s_tile.f_score = s_tile.g_score + s_tile.h_score
    s_tile.open = 1
    print("Start tile %s" % (s_tile))
    heapq.heappush(open_set,(s_tile))
    try:
        while 1>0:
            current = heapq.heappop(open_set)
            if current.is_same(e_tile):
                print("Found path to %s" % (e_tile))
                return build_and_mark_path_to(e_tile)
            current.open = 0 # mark as reamoved from open
            current.closed = 1 # mark as closed
            neighbours_of_current = get_neigbours(current, agoniasMap)
            for neighbour in neighbours_of_current:
                if neighbour.closed == 1 or myDict.get(mvp_mods.tribe)[neighbour.terrain] == -1:
                    continue # this tile was already checked
                if not neighbour.open == 1:
                    tentative_g_score = current.g_score + step_cost(current,neighbour, mvp_mods)
                    heuristic_estimate = heuristic_estimate_of_distance_between(neighbour, e_tile)
                    neighbour.h_score = heuristic_estimate
                    neighbour.g_score = tentative_g_score
                    neighbour.f_score = tentative_g_score + heuristic_estimate
                    neighbour.prev = current
                    neighbour.open = 1
                    heapq.heappush(open_set,(neighbour))
                else:
                    if neighbour.g_score > current.g_score + step_cost(current,neighbour, mvp_mods):
                        tentative_g_score = current.g_score + step_cost(current,neighbour, mvp_mods)
                        heuristic_estimate = heuristic_estimate_of_distance_between(neighbour, e_tile)
                        neighbour.prev = current
                        neighbour.g_score = tentative_g_score
                        neighbour.f_score = tentative_g_score + heuristic_estimate

    except:
        print("No path found")

    pass

def find_path_bounds(path):
    first = path[0]
    bonds = [(first.row,first.row),(first.column,first.column)]
    for tile in path:
        if bonds[0][0] > tile.row:
            bonds[0] = (tile.row, bonds [0][1])
        if bonds[0][1] < tile.row:
            bonds[0] = (bonds [0][0],tile.row)
        if bonds[1][0] > tile.column:
            bonds[1] = (tile.column , bonds[1][1])
        if bonds[1][1] < tile.column:
            bonds[1] = (bonds[1][0],tile.column)

    return bonds


def do_magic(path):
    bonds = find_path_bounds(path)

    min_x=bonds[0][0]-1
    max_x=bonds[0][1]+2
    min_y=bonds[1][0]-1
    max_y=bonds[1][1]+2

    rows = []
    for row in range (min_x,max_x):
        columns_of_row = []
        for column in range (min_y,max_y):
            columns_of_row.append(agoniasMap.map_of_tiles[row,column].to_img())
        rows.append(columns_of_row)

    pixels = np.zeros(((max_x-min_x)*7, (max_y-min_y)*7, 3))
    for ii in range((max_x-min_x)*7):
        for jj in range ((max_y-min_y)*7):
            for zz in range(3):
                tt = rows[int(ii/7)][int(jj/7)]
                pixels[ii][jj][zz] = tt[ii%7][jj%7][zz]

    return pixels


mvp_mods = t.MvpMod("kiith", None, None)
#TODO ingame coordinast must be modified by -1 as arrays are indexed from 0
#TODO also ingame coords in oposit order row, coll then here
# ingame location 109,122 is in matrix agoniasMap.map_of_tiles[121,108]
# from(257,172) to (240, 148)
star_tile = agoniasMap.map_of_tiles[171,256]
end_tile = agoniasMap.map_of_tiles[147,239]

path = find_path(star_tile, end_tile, agoniasMap, mvp_mods)
pixels = do_magic(path)

img = Image.fromarray(np.uint8(pixels), 'RGB')
img.show()
