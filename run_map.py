import map
from map_util import STRUCTURE_TYPE, STRUCTURE_COLOR

terrain_layout = [6, 3, 4, 1, 2, 5]
terrain_rotate = [2, 5]
clues = [map.Clue('2_N_N_STONE'), map.Clue('2_N_BEAR_N'), map.Clue('0_FOREST-SWAMP_N_N')]

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