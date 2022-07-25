import map
from map_util import STRUCTURE_TYPE, STRUCTURE_COLOR

terrain_layout = [6, 3, 4, 1, 2, 5]
terrain_rotate = [2, 5]
clues_set = [map.Clue('0_FOREST-DESERT_N_N'), map.Clue('0_FOREST-WATER_N_N'), map.Clue('0_FOREST-SWAMP_N_N'), map.Clue('0_FOREST-MOUNTAIN_N_N'),
            map.Clue('0_DESERT-WATER_N_N'), map.Clue('0_DESERT-SWAMP_N_N'), map.Clue('0_DESERT-MOUNTAIN_N_N'), 
            map.Clue('0_WATER-SWAMP_N_N'), map.Clue('0_WATER-MOUNTAIN_N_N'),
            map.Clue('0_SWAMP-MOUNTAIN_N_N'),
            map.Clue('1_FOREST_N_N'), map.Clue('1_DESERT_N_N'), map.Clue('1_SWAMP_N_N'), 
            map.Clue('1_MOUNTAIN_N_N'), map.Clue('1_WATER_N_N'), map.Clue('1_N_BEAR-COUGAR_N'), 
            map.Clue('2_N_N_STONE'), map.Clue('2_N_N_SHACK'), map.Clue('2_N_COUGAR_N'), map.Clue('2_N_BEAR_N'),
            map.Clue('3_N_N_BLUE'), map.Clue('3_N_N_WHITE'), map.Clue('3_N_N_GREEN'),
]

clues_id = [15, 16, 17, 19, 20, 22]
clues = [clues_set[x] for x in clues_id]

# [map.Clue('0_FOREST-SWAMP_N_N'), map.Clue('2_N_N_STONE') ,map.Clue('2_N_BEAR_N')]
# clues = [map.Clue('2_N_BEAR_N')]
# clues = [map.Clue('2_N_N_STONE')]

structure_sets = [
    [STRUCTURE_TYPE.SHACK, STRUCTURE_COLOR.WHITE, [0, 4]],
    [STRUCTURE_TYPE.SHACK, STRUCTURE_COLOR.BLUE, [-4, 11]],
    [STRUCTURE_TYPE.SHACK, STRUCTURE_COLOR.GREEN, [1, 10]],
    [STRUCTURE_TYPE.STONE, STRUCTURE_COLOR.WHITE, [6, 1]],
    [STRUCTURE_TYPE.STONE, STRUCTURE_COLOR.BLUE, [4, 7]],
    [STRUCTURE_TYPE.STONE, STRUCTURE_COLOR.GREEN, [1, 5]],
]

test_map = map.Map(terrain_layout, terrain_rotate, structure_sets, clues)

while test_map.main_loop():
    test_map.draw()

test_map.quit_app()