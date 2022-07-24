import numpy as np
import hexy as hx
import pygame as pg
from enum import Enum
from enum import IntEnum

TERRCOLORS = {
    'DESERT': np.array([255, 185, 15]),
    'FOREST': np.array([34, 139, 34]),
    'MOUNTAIN': np.array([169, 169, 169]),
    'SWAMP': np.array([148, 0, 211]),
    'WATER': np.array([85, 163, 193]),
    'NONE': np.array([255, 255, 255]),
}
    
STRUCTCOLORS = {
    'BLUE': np.array([53, 111, 163]),
    'WHITE': np.array([255, 255, 255]),
    'GREEN': np.array([0, 255, 0]),
    'BLACK': np.array([2, 0, 0]),
    'NONE' : np.array([0,0,0])
}

ANIMALCOLORS = {
    'NONE' :   np.array([0,0,0]),
    'BEAR' :   np.array([2,0,0]),
    'COUGAR' : np.array([255,0,0]),
    }

class TERRAIN(Enum):
    DESERT   = 0
    FOREST   = 1
    MOUNTAIN = 2
    SWAMP    = 3
    WATER    = 4
    NONE     = 5
    
class ANIMAL(Enum):
    NONE   = 0
    BEAR   = 1
    COUGAR = 2
    
class STRUCTURE_TYPE(IntEnum):
    NONE  = 0
    SHACK = 3
    STONE = 8
    
class STRUCTURE_COLOR(Enum):
    BLUE   = 0
    WHITE  = 1
    GREEN  = 2
    BLACK  = 3
    NONE   = 4
    

NE = np.array((1, 0, -1))
NW = np.array((0, 1, -1))
W = np.array((-1, 1, 0))
SW = np.array((-1, 0, 1))
SE = np.array((0, -1, 1))
E = np.array((1, -1, 0))
ALL_DIRECTIONS = np.array([NW, NE, E, SE, SW, W])

terrain_sets = {
    1: [
        TERRAIN.SWAMP, TERRAIN.SWAMP, TERRAIN.WATER,
        TERRAIN.SWAMP, TERRAIN.SWAMP, TERRAIN.WATER,
        TERRAIN.DESERT, TERRAIN.WATER, TERRAIN.WATER,
        TERRAIN.DESERT, TERRAIN.DESERT, TERRAIN.WATER,
        TERRAIN.DESERT, TERRAIN.FOREST, TERRAIN.FOREST,
        TERRAIN.FOREST, TERRAIN.FOREST, TERRAIN.FOREST
    ],
    2: [
        TERRAIN.SWAMP, TERRAIN.SWAMP, TERRAIN.SWAMP,
        TERRAIN.MOUNTAIN, TERRAIN.SWAMP, TERRAIN.FOREST,
        TERRAIN.MOUNTAIN, TERRAIN.FOREST, TERRAIN.FOREST,
        TERRAIN.MOUNTAIN, TERRAIN.DESERT, TERRAIN.FOREST,
        TERRAIN.MOUNTAIN, TERRAIN.DESERT, TERRAIN.FOREST,
        TERRAIN.DESERT, TERRAIN.DESERT, TERRAIN.FOREST,
    ],
    3: [
        TERRAIN.MOUNTAIN, TERRAIN.SWAMP, TERRAIN.SWAMP,
        TERRAIN.MOUNTAIN, TERRAIN.SWAMP, TERRAIN.SWAMP,
        TERRAIN.MOUNTAIN, TERRAIN.FOREST, TERRAIN.FOREST,
        TERRAIN.MOUNTAIN, TERRAIN.MOUNTAIN, TERRAIN.FOREST,
        TERRAIN.WATER, TERRAIN.WATER, TERRAIN.FOREST,
        TERRAIN.WATER, TERRAIN.WATER, TERRAIN.WATER,
    ],
    4: [
        TERRAIN.DESERT, TERRAIN.DESERT, TERRAIN.DESERT,
        TERRAIN.DESERT, TERRAIN.DESERT, TERRAIN.DESERT,
        TERRAIN.DESERT, TERRAIN.MOUNTAIN, TERRAIN.MOUNTAIN,
        TERRAIN.FOREST, TERRAIN.WATER, TERRAIN.MOUNTAIN,
        TERRAIN.FOREST, TERRAIN.WATER, TERRAIN.MOUNTAIN,
        TERRAIN.FOREST, TERRAIN.WATER, TERRAIN.MOUNTAIN
    ],
    5: [
        TERRAIN.DESERT, TERRAIN.SWAMP, TERRAIN.SWAMP,
        TERRAIN.DESERT, TERRAIN.DESERT, TERRAIN.SWAMP,
        TERRAIN.WATER, TERRAIN.DESERT, TERRAIN.SWAMP,
        TERRAIN.WATER, TERRAIN.WATER, TERRAIN.MOUNTAIN,
        TERRAIN.WATER, TERRAIN.MOUNTAIN, TERRAIN.MOUNTAIN,
        TERRAIN.WATER, TERRAIN.MOUNTAIN, TERRAIN.MOUNTAIN,
    ],
    6: [
        TERRAIN.MOUNTAIN, TERRAIN.MOUNTAIN, TERRAIN.DESERT,
        TERRAIN.WATER, TERRAIN.MOUNTAIN, TERRAIN.DESERT,
        TERRAIN.WATER, TERRAIN.SWAMP, TERRAIN.SWAMP,
        TERRAIN.WATER, TERRAIN.SWAMP, TERRAIN.SWAMP,
        TERRAIN.WATER, TERRAIN.FOREST, TERRAIN.SWAMP,
        TERRAIN.FOREST, TERRAIN.FOREST, TERRAIN.FOREST
    ]
}

structure_sets = [
    [STRUCTURE_TYPE.SHACK, STRUCTURE_COLOR.WHITE, [-2, 3]],
    [STRUCTURE_TYPE.SHACK, STRUCTURE_COLOR.BLUE, [-3, 5]],
    [STRUCTURE_TYPE.STONE, STRUCTURE_COLOR.GREEN, [3, 0]],
    [STRUCTURE_TYPE.STONE, STRUCTURE_COLOR.WHITE, [5, 2]],
    [STRUCTURE_TYPE.STONE, STRUCTURE_COLOR.BLUE, [1, 4]],
    [STRUCTURE_TYPE.SHACK, STRUCTURE_COLOR.GREEN, [4, 5]],
]

animal_sets = [
    [ANIMAL.COUGAR, [-1, 4]],
    [ANIMAL.COUGAR, [-1, 5]],
    [ANIMAL.COUGAR, [-2, 5]],
    [ANIMAL.COUGAR, [-6, 11]],
    [ANIMAL.COUGAR, [-5, 10]],
    [ANIMAL.COUGAR, [-5, 9]],
    [ANIMAL.COUGAR, [1, 11]],
    [ANIMAL.COUGAR, [0, 11]],
    [ANIMAL.COUGAR, [0, 1]],
    [ANIMAL.BEAR, [4, 0]],
    [ANIMAL.BEAR, [5, 0]],
    [ANIMAL.BEAR, [4, 1]],
    [ANIMAL.BEAR, [7, 0]],
    [ANIMAL.BEAR, [8, 0]],
    [ANIMAL.BEAR, [-2, 9]],
    [ANIMAL.BEAR, [-2, 10]],
]

def make_poly_surface(color, shape = 6, angle_start = 45, sf = 1, radius = 30, opacity = 255, border_color=(100, 100, 100), border=True, hollow=False):
    """
    Draws a hexagon with gray borders on a pygame surface.
    :param terr: The terrain of the hex which determines its color.
    :param animal: The animal type of the hex which determines the inner border
    :param structure_type: The structure type associated with the hex
    :param structure_color: The structure color associated with the hex
    :param radius: The radius (from center to any corner) of the hexagon.
    :param opacity: Number from 0 to 255 describing opacity of fill color
    :param border_color: Color of the border.
    :param border: Draws border if True
    :param hollow: Does not fill hex with color if True.
    
    :return: A pygame surface with a hexagon drawn on it
    """

    angles_in_radians = np.deg2rad([(360 // shape) * i + angle_start for i in range(shape)])
    x = sf * radius * np.cos(angles_in_radians)
    y = sf * radius * np.sin(angles_in_radians)
    points = np.round(np.vstack([x, y]).T)

    sorted_x = sorted(points[:, 0])
    sorted_y = sorted(points[:, 1])
    minx = sorted_x[0]
    maxx = sorted_x[-1]
    miny = sorted_y[0]
    maxy = sorted_y[-1]

    sorted_idxs = np.lexsort((points[:, 0], points[:, 1]))
    
    # Main surface dimensions
    surf_size = np.array((maxx - minx, maxy - miny)) * 2 + 1
    center = surf_size / 2
    surface = pg.Surface(surf_size)
    surface.set_colorkey((0, 0, 0))

    # Set fill color of shape and opacity of fill.
    surface.set_alpha(opacity)

    # fill if not hollow.
    if not hollow:
        pg.draw.polygon(surface, color, points + center, 0)


    points[sorted_idxs[-1:-4:-1]] += [0, 1]
    
    # if border is true is true draw border.
    
    if border or hollow:
        pg.draw.lines(surface, border_color, True, points + center, 1)

    return surface


def translate_coord(coord, direction, distance):
    direction = hx.cube_to_axial(np.array([direction]))

    for i in range(len(coord)):
        coord[i] = coord[i] + distance * np.squeeze(direction)

    return coord


def gen_hex_rectangle(size, center):
    width = size[0]
    height = size[1]

    center_q = center[0]
    center_r = center[1]

    coord = []
    for row in range(height):
        for col in range(width):
            if row % 2 != 0:
                offset = 1
            else:
                offset = 0
            coord.append(
                [col - row//2 - offset + center_q, row + center_r]
            )       
            

    return np.array(coord)


def get_map_cell_coord(cell_i):
    coord = []

    coord = gen_hex_rectangle(size = (3, 6), center = ((cell_i % 3 ) * 3 - (cell_i // 3 ) * 3, (cell_i // 3 ) * 6))

    # coord = translate_map(coord, W, 1)
    # coord = translate_map(coord, NW, 5)

    return coord

def rotate_terrain(terrain_set):
    terrain_set = np.reshape(np.array(terrain_set), (6, 3))
    terrain_set = np.flipud(np.fliplr(terrain_set)).flatten()
    return terrain_set


