import numpy as np
import hexy as hx
import pygame as pg
import map_util as mut
import os
from enum import Enum, auto, IntEnum
from typing import List

class ter(Enum):
    M = auto()
    S = auto()
    F = auto()
    D = auto()
    W = auto()

class Map:
    def __init__(self):
        self.hex_map = hx.HexMap()
        
        self.size = np.array([1200, 1200])
        self.width, self.height = self.size
        self.center = self.size / 2

        terrain_rotate = [3, 4, 6, 1]

        for i, cell_i in enumerate([3, 4, 2, 6, 5, 1]):
            coord = mut.get_map_cell_coord(i)

            hex_radius = 30

            hexes = []

            if cell_i in terrain_rotate:
                terrain_set = mut.rotate_terrain(mut.terrain_sets[cell_i])
            else:
                terrain_set = mut.terrain_sets[cell_i]

            for hex_i, x in enumerate(coord):
                
                color = list(mut.TERRCOLORS.keys())[terrain_set[hex_i].value]

                temp_hex = hexagon(
                                x,
                                color,
                                hex_radius
                            )
                
                hexes.append(temp_hex)

                for struct in mut.structure_sets:
                    if np.array_equal(np.array(struct[2]) , x):
                        structure = (struct[0].value, 
                            list(mut.STRUCTCOLORS.keys())[struct[1].value])
                        temp_hex.add_structure(structure[0], structure[1])

                for animals in mut.animal_sets:
                    if np.array_equal(np.array(animals[1]) , x):
                        animal = list(mut.ANIMALCOLORS.keys())[animals[0].value]
                        temp_hex.add_animal(animal)

            self.hex_map[np.array(coord)] = hexes


        # Init pygame variables
        self.main_surf = None
        self.font = None
        self.clock = None
        self.init_pg()


    def init_pg(self):
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (200, 200)

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
        # sorted_indexes = np.argsort(hex_positions[:, 1, :])
        
        for index in range(np.shape(hex_positions)[0]):
            self.main_surf.blit(hexagons[index].image, hex_positions[index][0] + self.center)
            if hexagons[index].animal.value:
                self.main_surf.blit(hexagons[index].inner, hex_positions[index][1] + self.center)
            if hexagons[index].structure_type:
                self.main_surf.blit(hexagons[index].object, hex_positions[index][2] + self.center)

        for hexagon in list(self.hex_map.values()):
            check_hex(self.hex_map, hexagon)

            text = self.font.render(str(hexagon.clue_valid), False, (0, 0, 0))
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
    
class hexagon(hx.HexTile):
    def __init__(self, axial_coordinates, terrain, radius):
        self.axial_coordinates = np.array([axial_coordinates])
        self.cube_coordinates = hx.axial_to_cube(self.axial_coordinates)
        self.radius = radius
        self.position = hx.axial_to_pixel(self.axial_coordinates, radius = self.radius)
        self.terrain = mut.TERRAIN[terrain]
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

        # flag if cryptid
        
        
    def add_structure(self, struct, color):
        self.structure_type = struct
        self.structure_color = mut.STRUCTURE_COLOR[color]
        
        self.object = mut.make_poly_surface(mut.STRUCTCOLORS[list(mut.STRUCTCOLORS.keys())[self.structure_color.value]],
                                            border_color = mut.STRUCTCOLORS[list(mut.STRUCTCOLORS.keys())[self.structure_color.value]],
                                            shape = self.structure_type,
                                            sf = 1/2,
                                            radius = self.radius,
                                            angle_start = 60
                                            )
    
    def add_animal(self, animal):
        self.animal = mut.ANIMAL[animal]
        
        self.inner = mut.make_poly_surface(mut.TERRCOLORS[list(mut.TERRCOLORS.keys())[self.terrain.value]],
                                           border_color = mut.ANIMALCOLORS[list(mut.ANIMALCOLORS.keys())[self.animal.value]], 
                                           sf = 5/6, 
                                           opacity = 255,
                                           radius = self.radius,
                                           angle_start = 30,
                                           hollow = True
                                           )

    def set_terrain(self, terr):
        # terr is a string in all caps
        self.terrain = mut.TERRAIN[terr]
        
        self.image = mut.make_poly_surface(mut.TERRCOLORS[list(mut.TERRCOLORS.keys())[self.terrain.value]],
                                           shape = self.structure_type,
                                           radius = self.radius,
                                           angle_start = 30
                                           )

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


def check_terrain(hex: hexagon, terrains: List[Enum]):
    clue_valid = (hex.terrain in terrains)
    return clue_valid

def check_animal(hex: hexagon):
    clue_valid = (hex.animal in mut.ANIMAL) and (hex.animal is not mut.ANIMAL.NONE)
    return clue_valid

def check_structure_type(hex: hexagon):
    clue_valid = (hex.structure_type in mut.STRUCTURE_TYPE) and (hex.animal is not mut.STRUCTURE_TYPE.NONE)
    return clue_valid

def check_within(map, hex: hexagon, check: Enum, radius=0):
    center = hex.axial_coordinates
    check_coord = []
    clue_valid = False

    for q in np.linspace(-radius, radius, int(2*radius+1), dtype=int):
        for r in np.linspace(-radius, radius, int(2*radius+1), dtype=int):
            if abs(q + r) <= radius:
                check_coord.append((center + [q, r]))

    for coord in check_coord:
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

def check_hex(map, hex):
    hex.clue_valid = ((check_within(map, hex, mut.ANIMAL.BEAR, radius = 2)) and
                    (check_within(map, hex, mut.TERRAIN.FOREST) or check_within(map, hex, mut.TERRAIN.DESERT)) and
                    (check_within(map, hex, mut.STRUCTURE_COLOR.GREEN, radius = 3))
    )

    return hex.clue_valid

# def translate_map(map, direction, distance):
#     direction = hx.cube_to_axial(np.array([direction]))
#     print(type(map))
#     temp_map = map
#     for hex_coord in temp_map:
#         hex_coord = np.fromstring(hex_coord, dtype=int, sep=',')
#         hex = map[hex_coord][0]
#         print(hex)

#         print(hex.axial_coordinates)
#         old_coord = hex.axial_coordinates

#         hex.axial_coordinates += distance * np.squeeze(direction)

#         print(hex.axial_coordinates)

# # self.hex_map[np.array(coord)] = hexes
#         del map[old_coord]
#         print(map[hex.axial_coordinates])
#         map[hex.axial_coordinates] = [hex]

#         # print(hex_coord, distance, np.squeeze(direction))
#         # print(hex_coord + distance * np.squeeze(direction))
#         # map[hex_coord + distance * np.squeeze(direction)] = map[hex_coord]

#     return map