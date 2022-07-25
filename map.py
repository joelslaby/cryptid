import numpy as np
import hexy as hx
import pygame as pg
import map_util as mut
import os
from enum import Enum, auto
from typing import List
from itertools import combinations

class ter(Enum):
    M = auto()
    S = auto()
    F = auto()
    D = auto()
    W = auto()

class Map:
    def __init__(self, terrain_layout, terrain_rotate, structure_sets, player_nbr, clues):
        self.hex_map = hx.HexMap()
        self.size = np.array([600, 650])
        self.width, self.height = self.size
        self.center = np.array([100, 75])
        self.hex_radius = 30

        self.terrain_rotate = terrain_rotate
        self.terrain_layout = terrain_layout
        self.structure_sets = structure_sets
        self.player_nbr = player_nbr
        self.clues = clues

        for i, cell_i in enumerate(self.terrain_layout):
            coord = mut.get_map_cell_coord(i)

            hexes = []

            if cell_i in self.terrain_rotate:
                terrain_set = mut.rotate_terrain(mut.terrain_sets[cell_i])
            else:
                terrain_set = mut.terrain_sets[cell_i]

            for hex_i, x in enumerate(coord):

                color = list(mut.TERRCOLORS.keys())[terrain_set[hex_i].value]

                temp_hex = hexagon(
                                x,
                                color,
                                self.hex_radius
                            )

                hexes.append(temp_hex)

                for struct in self.structure_sets:
                    if np.array_equal(np.array(struct[2]) , x):
                        structure = (struct[0].value,
                            list(mut.STRUCTCOLORS.keys())[struct[1].value])
                        temp_hex.add_structure(structure[0], structure[1])

                for animals in mut.animal_sets[cell_i]:
                    if cell_i in self.terrain_rotate:
                        cell_center = -np.array(animals[1]) + np.array([-1, 5])
                    else:
                        cell_center = np.array(animals[1])
                    if np.array_equal(cell_center + coord[0], x):
                        animal = list(mut.ANIMALCOLORS.keys())[animals[0].value]
                        temp_hex.add_animal(animal)

            self.hex_map[np.array(coord)] = hexes


        # Init pygame variables
        self.main_surf = None
        self.font = None
        self.clock = None
        self.init_pg()

    # Creates window to display map
    def init_pg(self):
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (200, 200)

        pg.init()
        self.main_surf = pg.display.set_mode(self.size, 0, 0)

        pg.font.init()
        self.font = pg.font.SysFont("monospace", 14, True)
        self.clock = pg.time.Clock()

    # Adds two methods for stopping program
    def handle_events(self):
        running = True
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.KEYUP:
                if event.key == pg.K_ESCAPE:
                    running = False

        return running

    # Constantly checks for the quit methods
    def main_loop(self):
        running = self.handle_events()

        return running

    # Draws hex tiles based on their axial coordinates
    def draw(self):
        self.main_surf.fill('white') # Makes white background for window
        self.clock.tick(30) # Sets frame rate of window

        hexagons = list(self.hex_map.values())
        hex_positions = np.array([hexagon.get_draw_position() for hexagon in hexagons])
        # sorted_indexes = np.argsort(hex_positions[:, 1, :])

        for index in range(np.shape(hex_positions)[0]):
            self.main_surf.blit(hexagons[index].image, hex_positions[index][0] + self.center)
            if hexagons[index].animal.value:
                self.main_surf.blit(hexagons[index].inner, hex_positions[index][1] + self.center)
            if hexagons[index].structure_type:
                self.main_surf.blit(hexagons[index].object, hex_positions[index][2] + self.center)

        find_clues(self.hex_map, self.clues, numPlayers = self.player_nbr)

        for hexagon in list(self.hex_map.values()):
            x = check_hex(self.hex_map, hexagon, self.clues)

            # np.sum(clue_data_vect)
            text = self.font.render(str(int(x)), False, (0, 0, 0))
            text.set_alpha(160)
            text_pos = hexagon.get_position() + self.center
            text_pos -= (text.get_width() / 2, text.get_height() / 2)
            self.main_surf.blit(text, text_pos)

        # print(clue_data[0])

        pg.display.update() # Update screen at 30 frames per second
        pg.image.save(self.main_surf, 'test.png') # Saves image as 'test.png' before program closes window

        self.quit_app() # Quits app at the end of the draw

    def quit_app(self):
        pg.quit()
        raise SystemExit

class hexagon(hx.HexTile):
    def __init__(self, axial_coordinates, terrain, radius):
        self.axial_coordinates = np.array([axial_coordinates])
        self.cube_coordinates = hx.axial_to_cube(self.axial_coordinates)
        self.radius = radius
        self.position = hx.axial_to_pixel(self.axial_coordinates, radius = self.radius)
        self.terrain = mut.TERRAIN[terrain] # Intended to pull terrain from map_util.py terrain_sets
        self.animal = mut.ANIMAL['NONE']
        self.structure_type = mut.STRUCTURE_TYPE['NONE']
        self.structure_color = mut.STRUCTURE_COLOR['NONE']
        self.inner = None
        self.object = None
        self.image = mut.make_poly_surface(mut.TERRCOLORS[list(mut.TERRCOLORS.keys())[self.terrain.value]],
                                           radius = self.radius,
                                           angle_start = 30
                                           )
        self.clue_valid = 1

    # Sets the structure parameters and draws them on the map for their respective hexes
    def add_structure(self, struct, color):
        self.structure_type = struct # Intended to take structure from STRUCTURE_TYPE in map.util.py
        self.structure_color = mut.STRUCTURE_COLOR[color] # Intended to take animal from STRUCTURE_COLOR in map_util.py

        self.object = mut.make_poly_surface(mut.STRUCTCOLORS[list(mut.STRUCTCOLORS.keys())[self.structure_color.value]],
                                            border_color = mut.STRUCTCOLORS[list(mut.STRUCTCOLORS.keys())[self.structure_color.value]],
                                            shape = self.structure_type,
                                            sf = 1/2,
                                            radius = self.radius,
                                            angle_start = 60
                                            )

    # Sets the animal parameters and draws them on the map for their respective hexes
    def add_animal(self, animal):
        self.animal = mut.ANIMAL[animal] # Intended to take animal from animal_sets in map_util.py

        # Draws border around selected hex of appropriate colors
        self.inner = mut.make_poly_surface(mut.TERRCOLORS[list(mut.TERRCOLORS.keys())[self.terrain.value]],
                                           border_color = mut.ANIMALCOLORS[list(mut.ANIMALCOLORS.keys())[self.animal.value]],
                                           sf = 5/6,
                                           opacity = 255,
                                           radius = self.radius,
                                           angle_start = 30,
                                           hollow = True
                                           )
    """
    # NEVER USED
    # Sets the terrain parameters and fills them on the map for their respective hexes
    def set_terrain(self, terr):
        self.terrain = mut.TERRAIN[terr] # terr is a string in all caps
        # Draws the infill of the given hex with the appropriate colors
        self.image = mut.make_poly_surface(mut.TERRCOLORS[list(mut.TERRCOLORS.keys())[self.terrain.value]],
                                           shape = self.structure_type,
                                           radius = self.radius,
                                           angle_start = 30
                                           )
    """

    def get_draw_position(self):
        """
        Get the location to draw this hex so that the center of the hex is at `self.position`.
        :return: The location to draw this hex so that the center of the hex is at `self.position`.
        """

        draw_position = np.zeros((3,2))
        draw_position[0] = self.position[0] - [self.image.get_width() / 2, self.image.get_height() / 2]
        if (self.inner):
            draw_position[1] = self.position[0] - [self.inner.get_width() / 2, self.inner.get_height() / 2]
        if (self.object):
            draw_position[2] = self.position[0] - [self.object.get_width() / 2, self.object.get_height() / 2]

        return draw_position

    def get_position(self):
        """
        Retrieves the location of the center of the hex.
        :return: The location of the center of the hex.
        """
        return self.position[0]

    """
    # NEVER USED
    def check_terrain(hex: hexagon, terrains: List[Enum]):
        clue_valid = (hex.terrain in terrains)
        return clue_valid

    def check_animal(hex: hexagon):
        clue_valid = (hex.animal in mut.ANIMAL) and (hex.animal is not mut.ANIMAL.NONE)
        return clue_valid

    def check_structure_type(hex: hexagon):
        clue_valid = (hex.structure_type in mut.STRUCTURE_TYPE) and (hex.animal is not mut.STRUCTURE_TYPE.NONE)
        return clue_valid
    """

def check_within(map, hex: hexagon, check: Enum, radius=0):
    center = hex.axial_coordinates
    check_coord = []
    clue_valid = False

    for q in np.linspace(-radius, radius, int(2*radius+1), dtype=int):
        for r in np.linspace(-radius, radius, int(2*radius+1), dtype=int):
            if abs(q + r) <= radius:
                check_coord.append((center + [q, r]))

    for coord in check_coord: # Compares coordinate of hex tile with designated coordinates of items in
        if map[coord]:
            check_hex = map[coord][0]
            if check in mut.TERRAIN:
                clue_valid = clue_valid or (check_hex.terrain in [check])
            elif check in mut.ANIMAL:
                clue_valid = clue_valid or ((check_hex.animal in [check]) and (check_hex.animal is not mut.ANIMAL.NONE))
            elif check in mut.STRUCTURE_TYPE:
                clue_valid = clue_valid or ((check_hex.structure_type in [check]) and (check_hex.structure_type is not mut.STRUCTURE_TYPE.NONE))
            elif check in mut.STRUCTURE_COLOR:
                clue_valid = clue_valid or ((check_hex.structure_color in [check]) and (check_hex.structure_color is not mut.STRUCTURE_COLOR.NONE))

    return clue_valid

def check_hex(map, hex, clue_vect):

    for clue in clue_vect:
        temp_clue_valid = False
        rad, search = clue.check()
        if (type(search) == list):
            for s in search:
                temp_clue_valid = (temp_clue_valid or
                check_within(map, hex, s, radius = rad)
                )
            hex.clue_valid &= temp_clue_valid

        else:
            hex.clue_valid &= check_within(map, hex, search, radius = rad)

    return hex.clue_valid

def sweep_clues(map, hex, clue_vect):

    # Sweeps through all clues in clue_vect for a given hex on a map
    # Outputs binary vector for success/failure of clue in clue_vect
    # Standard game of Cryptid should output a 108x 23 vector

    clue_match = np.zeros(len(clue_vect))


    for (idx, clue) in enumerate(clue_vect):
        this_clue_valid = False

        rad, search = clue.check()

        if (type(search) == list):
            for s in search:
                this_clue_valid = (this_clue_valid or
                check_within(map, hex, s, radius = rad)
                )
        else:
            this_clue_valid = check_within(map, hex, search, radius = rad)

        clue_match[idx] = this_clue_valid


    return clue_match

def find_clues(map, clue_vect, numPlayers = 3):

    clue_data = []

    for hexagon in list(map.values()):
        clue_data.append(sweep_clues(map, hexagon, clue_vect))

    clue_data = np.array(clue_data, dtype = int)

    good_hexes = []
    good_clues = []

    for combo in combinations(clue_data.T, numPlayers):
        soln = combo[0]
        for clue_row in combo:
            soln = np.bitwise_and(soln, clue_row)
        if sum(soln) == 1:
            good_hexes.append(np.where(soln == 1)[0][0])

            clue_idx = []
            for clue_row in combo:
                clue_idx.append(np.where((clue_data.T == clue_row).all(axis=1))[0][0])

            good_clues.append(clue_idx)

    print(good_hexes, good_clues)
    print(len(good_hexes), len(good_clues))

    return good_hexes, good_clues



class Clue():
    def __init__(self, clue):

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

        # Splits clues separated by '_' into a list
        parsed = clue.split('_')
        clue_inputs = []

        for i in parsed:
            if i  == 'N':
                clue_inputs.append('NONE')
            else:
                clue_inputs.append(i)

        parsed_terrains = clue_inputs[1].split('-')
        parsed_animals = clue_inputs[2].split('-')

        # Designates clue attribute according to generated list
        self.radius        = int(clue_inputs[0])
        self.terrain       = [mut.TERRAIN[x] for x in parsed_terrains]
        self.animal        = [mut.ANIMAL[x] for x in parsed_animals]

        if self.radius == 2:
            self.structure = mut.STRUCTURE_TYPE[clue_inputs[3]]
        else:
            self.structure = mut.STRUCTURE_COLOR[clue_inputs[3]]

# Returns hex radius and attribute according to clue parameters
    def check(self):

        rad = self.radius
        search = None

        if mut.TERRAIN.NONE not in self.terrain:
            search = self.terrain
        elif mut.ANIMAL.NONE not in self.animal:
            search = self.animal
        elif self.structure:
            search = self.structure

        return rad, search
