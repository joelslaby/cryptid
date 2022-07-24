import numpy as np
import hexy as hx
import pygame as pg
from enum import Enum

TERRCOLORS = {
    'desert': np.array([255, 185, 15]),
    'forest': np.array([34, 139, 34]),
    'mountain': np.array([169, 169, 169]),
    'swamp': np.array([148, 0, 211]),
    'water': np.array([85, 163, 193]),
    'none': np.array([255, 255, 255]),
}
    
STRUCTCOLORS = {
    'blue': np.array([53, 111, 163]),
    'white': np.array([255, 255, 255]),
    'green': np.array([0, 255, 0]),
}

ANIMALCOLORS = {
    'none' :   np.array([0,0,0,0]),
    'bear' :   np.array([0,0,0,255]),
    'cougar' : np.array([255,0,0,255]),
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
    
class STRUCTURE_TYPE(Enum):
    NONE  = 0
    SHACK = 1
    STONE = 2
    
class STRUCTURE_COLOR(Enum):
    BLUE   = 0
    WHITE  = 1
    GREEN  = 2
    BLACK  = 3
    

NE = np.array((1, 0, -1))
NW = np.array((0, 1, -1))
W = np.array((-1, 1, 0))
SW = np.array((-1, 0, 1))
SE = np.array((0, -1, 1))
E = np.array((1, -1, 0))

terrain_sets = [
    [
        TERRAIN.WATER, TERRAIN.WATER, TERRAIN.WATER,
        TERRAIN.FOREST, TERRAIN.WATER, TERRAIN.WATER,
        TERRAIN.FOREST, TERRAIN.MOUNTAIN, TERRAIN.MOUNTAIN,
        TERRAIN.FOREST, TERRAIN.FOREST, TERRAIN.MOUNTAIN,
        TERRAIN.SWAMP, TERRAIN.SWAMP, TERRAIN.MOUNTAIN,
        TERRAIN.SWAMP, TERRAIN.SWAMP, TERRAIN.MOUNTAIN
    ],
    [
        TERRAIN.MOUNTAIN, TERRAIN.MOUNTAIN, TERRAIN.WATER,
        TERRAIN.MOUNTAIN, TERRAIN.MOUNTAIN, TERRAIN.WATER,
        TERRAIN.MOUNTAIN, TERRAIN.WATER, TERRAIN.WATER,
        TERRAIN.SWAMP, TERRAIN.DESERT, TERRAIN.WATER,
        TERRAIN.SWAMP, TERRAIN.DESERT, TERRAIN.DESERT,
        TERRAIN.SWAMP, TERRAIN.SWAMP, TERRAIN.DESERT
    ],
    [
        TERRAIN.MOUNTAIN, TERRAIN.MOUNTAIN, TERRAIN.DESERT,
        TERRAIN.WATER, TERRAIN.MOUNTAIN, TERRAIN.DESERT,
        TERRAIN.WATER, TERRAIN.SWAMP, TERRAIN.SWAMP,
        TERRAIN.WATER, TERRAIN.SWAMP, TERRAIN.SWAMP,
        TERRAIN.WATER, TERRAIN.FOREST, TERRAIN.SWAMP,
        TERRAIN.FOREST, TERRAIN.FOREST, TERRAIN.FOREST
    ],
    [
        TERRAIN.FOREST, TERRAIN.DESERT, TERRAIN.DESERT,
        TERRAIN.FOREST, TERRAIN.DESERT, TERRAIN.MOUNTAIN, 
        TERRAIN.FOREST, TERRAIN.DESERT, TERRAIN.MOUNTAIN,
        TERRAIN.FOREST, TERRAIN.FOREST, TERRAIN.MOUNTAIN,
        TERRAIN.FOREST, TERRAIN.SWAMP, TERRAIN.MOUNTAIN,
        TERRAIN.SWAMP, TERRAIN.SWAMP, TERRAIN.SWAMP
    ],
    [
        TERRAIN.SWAMP, TERRAIN.SWAMP, TERRAIN.WATER,
        TERRAIN.SWAMP, TERRAIN.SWAMP, TERRAIN.WATER,
        TERRAIN.DESERT, TERRAIN.WATER, TERRAIN.WATER,
        TERRAIN.DESERT, TERRAIN.DESERT, TERRAIN.DESERT,
        TERRAIN.DESERT, TERRAIN.FOREST, TERRAIN.FOREST,
        TERRAIN.FOREST, TERRAIN.FOREST, TERRAIN.FOREST
    ],
    [
        TERRAIN.DESERT, TERRAIN.DESERT, TERRAIN.DESERT,
        TERRAIN.DESERT, TERRAIN.DESERT, TERRAIN.DESERT,
        TERRAIN.DESERT, TERRAIN.MOUNTAIN, TERRAIN.MOUNTAIN,
        TERRAIN.FOREST, TERRAIN.WATER, TERRAIN.MOUNTAIN,
        TERRAIN.FOREST, TERRAIN.WATER, TERRAIN.MOUNTAIN,
        TERRAIN.FOREST, TERRAIN.WATER, TERRAIN.MOUNTAIN
    ]
]

def make_hex_surface(terr, shape = 6, radius = 20, opacity = 255, border_color=(100, 100, 100), border=True, hollow=False):
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
    angles_in_radians = np.deg2rad([60 * i + 30 for i in range(shape)])
    x = radius * np.cos(angles_in_radians)
    y = radius * np.sin(angles_in_radians)
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

    # Set fill color of terrain and opacity of fill.
    color = TERRCOLORS[terr]
    surface.set_alpha(opacity)

    # fill if not hollow.
    if not hollow:
        pg.draw.polygon(surface, color, points + center, 0)


    points[sorted_idxs[-1:-4:-1]] += [0, 1]
    
    # if border is true is true draw border.
    
    if border:
        pg.draw.lines(surface, border_color, True, points + center, 1)

    return surface


def translate_map(map, direction, distance):
    direction = hx.cube_to_axial(np.array([direction]))

    for i in range(len(map)):
        map[i] = map[i] + distance * np.squeeze(direction)

    return map


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
    coord = translate_map(coord, W, 1)
    coord = translate_map(coord, NW, 5)

    return coord
