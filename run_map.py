import map
from map_util import STRUCTURE_TYPE, STRUCTURE_COLOR

terrain_layout = [1, 5, 4, 6, 2, 3]
terrain_rotate = [1, 4, 6, 3]
clues_set = [map.Clue('0_FOREST-DESERT_N_N'), map.Clue('0_FOREST-WATER_N_N'), map.Clue('0_FOREST-SWAMP_N_N'), map.Clue('0_FOREST-MOUNTAIN_N_N'),
            map.Clue('0_DESERT-WATER_N_N'), map.Clue('0_DESERT-SWAMP_N_N'), map.Clue('0_DESERT-MOUNTAIN_N_N'), 
            map.Clue('0_WATER-SWAMP_N_N'), map.Clue('0_WATER-MOUNTAIN_N_N'),
            map.Clue('0_SWAMP-MOUNTAIN_N_N'),
            map.Clue('1_FOREST_N_N'), map.Clue('1_DESERT_N_N'), map.Clue('1_SWAMP_N_N'), 
            map.Clue('1_MOUNTAIN_N_N'), map.Clue('1_WATER_N_N'), map.Clue('1_N_BEAR-COUGAR_N'), 
            map.Clue('2_N_N_STONE'), map.Clue('2_N_N_SHACK'), map.Clue('2_N_COUGAR_N'), map.Clue('2_N_BEAR_N'),
            map.Clue('3_N_N_BLUE'), map.Clue('3_N_N_WHITE'), map.Clue('3_N_N_GREEN'),
]
# 

# clues_id = [0, 16, 17]
# clues = [clues_set[x] for x in clues_id]
clues = clues_set

player_nbr = 3

# [map.Clue('0_FOREST-SWAMP_N_N'), map.Clue('2_N_N_STONE') ,map.Clue('2_N_BEAR_N')]
# clues = [map.Clue('2_N_BEAR_N')]
# clues = [map.Clue('2_N_N_STONE')]

# structure_sets = [
#     [STRUCTURE_TYPE.SHACK, STRUCTURE_COLOR.WHITE, [0, 4]],
#     [STRUCTURE_TYPE.SHACK, STRUCTURE_COLOR.BLUE, [-4, 11]],
#     [STRUCTURE_TYPE.SHACK, STRUCTURE_COLOR.GREEN, [1, 10]],
#     [STRUCTURE_TYPE.STONE, STRUCTURE_COLOR.WHITE, [6, 1]],
#     [STRUCTURE_TYPE.STONE, STRUCTURE_COLOR.BLUE, [4, 7]],
#     [STRUCTURE_TYPE.STONE, STRUCTURE_COLOR.GREEN, [1, 5]],
# ]

structure_sets = [
    [STRUCTURE_TYPE.SHACK, STRUCTURE_COLOR.WHITE, [3, 2]],
    [STRUCTURE_TYPE.SHACK, STRUCTURE_COLOR.BLUE, [1, 1]],
    [STRUCTURE_TYPE.SHACK, STRUCTURE_COLOR.GREEN, [-2, 11]],
    [STRUCTURE_TYPE.STONE, STRUCTURE_COLOR.WHITE, [0, 5]],
    [STRUCTURE_TYPE.STONE, STRUCTURE_COLOR.BLUE, [7, 1]],
    [STRUCTURE_TYPE.STONE, STRUCTURE_COLOR.GREEN, [1, 6]],
]

test_map = map.Map(terrain_layout, terrain_rotate, structure_sets, player_nbr, clues, quit=True)

while test_map.main_loop():
    test_map.draw()

test_map.quit_app()