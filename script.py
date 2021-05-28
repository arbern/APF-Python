import numpy as np
import heapq
import t

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


def step_cost(current, neighbour, mvp_mods):
    straight_step_cost = get_straight_step_cost(neighbour.terrain, mvp_mods)
    if current.row==neighbour.row or current.column == neighbour.column: # stright step
        return straight_step_cost
    else:
        return int(round(1.41 * straight_step_cost))


def heuristic_estimate_of_distance_between(start, end):
    lowest_diagonal_step_cost = 5
    lowest_straight_step_cost = 3
    x_diff = abs(start.row - end.row)
    y_diff = abs(start.column - end.column)
    number_of_diagonal_steps = min(x_diff, y_diff)
    number_of_straight_steps = abs(x_diff-y_diff)
    return number_of_diagonal_steps * lowest_diagonal_step_cost + number_of_straight_steps * lowest_straight_step_cost


def print_path_to(e_tile):
    if e_tile.prev == None:
        print(e_tile)
        return
    print("Calling %s" % (e_tile.prev))
    return print_path_to(e_tile.prev)


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
                print_path_to(e_tile)
                break
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
mvp_mods = t.MvpMod("kiith", None, None)
#TODO ingame coordinast must be modified by -1 as arrays are indexed from 0
#TODO also ingame coords in oposit order row, coll then here
# ingame location 109,122 is in matrix agoniasMap.map_of_tiles[121,108]
# from(257,172) to (240, 148)
star_tile = agoniasMap.map_of_tiles[171,256]
end_tile = agoniasMap.map_of_tiles[147,239]

find_path(star_tile, end_tile, agoniasMap, mvp_mods)
