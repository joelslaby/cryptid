import map
from map_util import STRUCTURE_TYPE, STRUCTURE_COLOR

# Layout of the Cryptid Modules as made in map_util.py
terrain_layout = [6, 3, 4, 1, 2, 5]

# Rotates specified modules 180 degrees
terrain_rotate = [2, 5]

# All possible clues
"""
Documentation: The clue must take the following format: R_T_A_S

    - R (Radius)     : radius from the specified hex type within
                       which the cryptid exists
    - T (Terrain)    : Enum ID of terrain if specified
    - A (Animal)     : Enum ID of animal if specified
    - S (Structure)  : Enum ID of structure type or color if specified

    If the entry is not specified, put 'N' for NONE, as in:
        '3_N_N_GREEN' --> "Within 3 spaces from a GREEN STRUCTURE_COLOR"
        '1_DESERT_N_N' --> "Within 1 space of DESERT TERRAIN"
"""

clues_set = [map.Clue('0_FOREST-DESERT_N_N'),
            map.Clue('0_FOREST-WATER_N_N'),
            map.Clue('0_FOREST-SWAMP_N_N'),
            map.Clue('0_FOREST-MOUNTAIN_N_N'),
            map.Clue('0_DESERT-WATER_N_N'),
            map.Clue('0_DESERT-SWAMP_N_N'),
            map.Clue('0_DESERT-MOUNTAIN_N_N'),
            map.Clue('0_WATER-SWAMP_N_N'),
            map.Clue('0_WATER-MOUNTAIN_N_N'),
            map.Clue('0_SWAMP-MOUNTAIN_N_N'),

            map.Clue('1_FOREST_N_N'),
            map.Clue('1_DESERT_N_N'),
            map.Clue('1_SWAMP_N_N'),
            map.Clue('1_MOUNTAIN_N_N'),
            map.Clue('1_WATER_N_N'),
            map.Clue('1_N_BEAR-COUGAR_N'),

            map.Clue('2_N_N_STONE'),
            map.Clue('2_N_N_SHACK'),
            map.Clue('2_N_COUGAR_N'),
            map.Clue('2_N_BEAR_N'),
            map.Clue('3_N_N_BLUE'),
            map.Clue('3_N_N_WHITE'),
            map.Clue('3_N_N_GREEN'),
]


#Comment for generating clues, uncomment for finding on map
clues_id = [2, 13, 14, 18, 20]
clues = [clues_set[x] for x in clues_id]

#Uncomment for generating clues, comment for finding on map
#clues = clues_set

# Specifies how many players within the game
player_nbr = 5

# [map.Clue('0_FOREST-SWAMP_N_N'), map.Clue('2_N_N_STONE') ,map.Clue('2_N_BEAR_N')]
# clues = [map.Clue('2_N_BEAR_N')]
# clues = [map.Clue('2_N_N_STONE')]


# Change for the placement of structures based on axial location
structure_sets = [
    [STRUCTURE_TYPE.SHACK, STRUCTURE_COLOR.WHITE, [0, 4]],
    [STRUCTURE_TYPE.SHACK, STRUCTURE_COLOR.BLUE, [-4, 11]],
    [STRUCTURE_TYPE.SHACK, STRUCTURE_COLOR.GREEN, [1, 10]],
    [STRUCTURE_TYPE.STONE, STRUCTURE_COLOR.WHITE, [6, 1]],
    [STRUCTURE_TYPE.STONE, STRUCTURE_COLOR.BLUE, [4, 7]],
    [STRUCTURE_TYPE.STONE, STRUCTURE_COLOR.GREEN, [1, 5]],
]

# Generates map
test_map = map.Map(terrain_layout, terrain_rotate, structure_sets, player_nbr, clues)

# Draws map
while test_map.main_loop():
    test_map.draw()

# Forces map window to close
test_map.quit_app()
