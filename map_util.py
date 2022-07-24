import numpy as np
import hexy as hx
import pygame as pg
from sympy import N

COLORS = {
    'red': np.array([244, 98, 105]),
    'orange': np.array([251, 149, 80]),
    'green': np.array([141, 207, 104]),
    'blueD': np.array([53, 111, 163]),
    'blueL': np.array([85, 163, 193]),
    'black': np.array([0, 0, 0]),
    'white': np.array([255, 255, 255])
}

NE = np.array((1, 0, -1))
NW = np.array((0, 1, -1))
W = np.array((-1, 1, 0))
SW = np.array((-1, 0, 1))
SE = np.array((0, -1, 1))
E = np.array((1, -1, 0))

def make_hex_surface(color, radius, border_color=(100, 100, 100), border=True, hollow=False):
    """
    Draws a hexagon with gray borders on a pygame surface.
    :param color: The fill color of the hexagon.
    :param radius: The radius (from center to any corner) of the hexagon.
    :param border_color: Color of the border.
    :param border: Draws border if True.
    :param hollow: Does not fill hex with color if True.
    :return: A pygame surface with a hexagon drawn on it
    """
    angles_in_radians = np.deg2rad([60 * i + 30 for i in range(6)])
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

    surf_size = np.array((maxx - minx, maxy - miny)) * 2 + 1
    center = surf_size / 2
    surface = pg.Surface(surf_size)
    surface.set_colorkey((0, 0, 0))

    # Set alpha if color has 4th coordinate.
    if len(color) >= 4:
        surface.set_alpha(color[-1])

    # fill if not hollow.
    if not hollow:
        pg.draw.polygon(surface, color, points + center, 0)


    points[sorted_idxs[-1:-4:-1]] += [0, 1]
    # if border is true or hollow is true draw border.
    if border or hollow:
        pg.draw.lines(surface, border_color, True, points + center, 1)

    return surface


def translate_map(map, direction, distance):
    direction = hx.cube_to_axial(np.array([direction]))

    for i in range(len(map)):
        map[i] = map[i] + distance * np.squeeze(direction)

    return map

def gen_hex_rectangle(width, height):
    coord = []
    for r in range(height):
        if r % 2 != 0:
            w = width - 1
        else:
            w = width
        
        for c in range(w):
            coord.append(
                [c - r//2, r]
            )           
            

    return np.array(coord)