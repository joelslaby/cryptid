# If module missing, use "pip install <module here>"



import numpy as np
import hexy as hx
import pygame as pg
import map_util as mut
import os
from enum import Enum, auto

class ter(Enum):
    M = auto()
    S = auto()
    F = auto()
    D = auto()
    W = auto()

class Map:
    def __init__(self):
        self.hex_map = hx.HexMap()
        self.size = np.array([700, 700])
        self.width, self.height = self.size
        self.center = self.size / 2

        for cell_i in range(6):
            coord = mut.get_map_cell_coord(cell_i)

            hex_radius = 30

            hexes = []
            for hex_i, x in enumerate(coord):

                color = list(mut.TERRCOLORS.keys())[mut.terrain_sets[cell_i][hex_i].value]

                hexes.append(
                    ExampleHex(
                        x,
                        color,
                        hex_radius
                    )
                )

            self.hex_map[np.array(coord)] = hexes

        # Init pygame variables
        self.main_surf = None
        self.font = None
        self.clock = None
        self.init_pg()


    def init_pg(self):
        # TODO: Dont hardcode
        # sets the window position to (x=100, y=100)
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100, 100)

        pg.init()
        self.main_surf = pg.display.set_mode(self.size, 0, 0)

        pg.font.init()
        self.font = pg.font.SysFont("monospace", 14, True)
        self.clock = pg.time.Clock()


    def handle_events(self):
        running = True
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.KEYUP:
                if event.key == pg.K_ESCAPE:
                    running = False

        return running


    def main_loop(self):
        running = self.handle_events()

        return running


    def draw(self):
        hexagons = list(self.hex_map.values())
        hex_positions = np.array([hexagon.get_draw_position() for hexagon in hexagons])
        sorted_indexes = np.argsort(hex_positions[:, 1])





        for index in sorted_indexes:
            self.main_surf.blit(hexagons[index].image, hex_positions[index] + self.center)

        for hexagon in list(self.hex_map.values()):
            text = self.font.render(str(hexagon.axial_coordinates[0]), False, (0, 0, 0))
            text.set_alpha(160)
            text_pos = hexagon.get_position() + self.center
            text_pos -= (text.get_width() / 2, text.get_height() / 2)
            self.main_surf.blit(text, text_pos)
        # Update screen at 30 frames per second
        pg.display.update()
        self.main_surf.fill('white')
        self.clock.tick(30)

    def quit_app(self):
        pg.quit()
        raise SystemExit

class ExampleHex(hx.HexTile):
    def __init__(self, axial_coordinates, color, radius):
        self.axial_coordinates = np.array([axial_coordinates])
        self.cube_coordinates = hx.axial_to_cube(self.axial_coordinates)
        self.position = hx.axial_to_pixel(self.axial_coordinates, radius)
        self.color = color
        self.radius = radius
        self.image = mut.make_hex_surface(color, radius = radius)
        self.value = None
        self.doesMatch = None

    def set_value(self, value):
        self.value = value

    def get_draw_position(self):
        """
        Get the location to draw this hex so that the center of the hex is at `self.position`.
        :return: The location to draw this hex so that the center of the hex is at `self.position`.
        """
        draw_position = self.position[0] - [self.image.get_width() / 2, self.image.get_height() / 2]
        return draw_position

    def get_position(self):
        """
        Retrieves the location of the center of the hex.
        :return: The location of the center of the hex.
        """
        return self.position[0]

# class hexagon(hx.HexTile):
#     def __init__(self, axial_coordinates):
#         self.axial_coordinates = np.array([axial_coordinates])
#         self.cube_coordinates = hx.axial_to_cube(self.axial_coordinates)
#         self.position = hx.axial_to_pixel(self.axial_coordinates, radius)
#         self.terrain = None
#         self.radius = 20
#         self.animal = None
#         self.structure_type = None
#         self.structure_color = None
#         self.image = mut.make_hex_surface(self.terrain, self.animal, self.structure_type, self.structure_color, radius = self.radius)

#     def set_terrain(self, terr_num):
#         self.terrain = TERRAIN(terr_num)

#     def get_draw_position(self):
#         """
#         Get the location to draw this hex so that the center of the hex is at `self.position`.
#         :return: The location to draw this hex so that the center of the hex is at `self.position`.
#         """
#         draw_position = self.position[0] - [self.image.get_width() / 2, self.image.get_height() / 2]
#         return draw_position

#     def get_position(self):
#         """
#         Retrieves the location of the center of the hex.
#         :return: The location of the center of the hex.
#         """
#         return self.position[0]
