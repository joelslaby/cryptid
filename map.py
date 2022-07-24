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
        # sorted_indexes = np.argsort(hex_positions[:, 1, :])
        
        for index in range(np.shape(hex_positions)[0]):
            self.main_surf.blit(hexagons[index].image, hex_positions[index][0] + self.center)
            if hexagons[index].animal.value:
                self.main_surf.blit(hexagons[index].inner, hex_positions[index][1] + self.center)
            if hexagons[index].structure_type:
                self.main_surf.blit(hexagons[index].object, hex_positions[index][2] + self.center)

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
