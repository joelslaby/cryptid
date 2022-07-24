from array import * #For arrays

# Clue List:
# Type 1: On one of two types of terrain
    # Detail 1: Forest/Desert
    # Detail 2: Forest/Water
    # Detail 3: Forest/Swamp
    # Detail 4: Forest/Mountain
    # Detail 5: Desert/Water
    # Detail 6: Desert/Swamp
    # Detail 7: Desert/Mountain
    # Detail 8: Water/Swamp
    # Detail 9: Water/Mountain
    # Detail 10: Swamp/Mountain

# Type 2: Within one space of terrain or animal territory
    # Detail 1: Forest
    # Detail 2: Desert
    # Detail 3: Swamp
    # Detail 4: Mountain
    # Detail 5: Animal

# Type 3: Within two spaces of animal or structure
    # Detail 1: Standing Stone
    # Detail 2: Abandoned Shack
    # Detail 3: Cougar
    # Detail 4: Bear

# Type 4: Within three spaces of structure color
    # Detail 1: Blue
    # Detail 2: White
    # Detail 3: Green

# Clue List (Dependency):
# Type 1: Animal
    # Detail 1: Within 1 of bear/Cougar
    # Detail 2: Within 2 of Bear
    # Detail 3: Within 2 of cougar
# Type 2: Structure
    # Detail 1: Within 2 of standing stone
    # Detail 2: Within 2 of abandoned shack
    # Detail 3: Within 3 of Green
    # Detail 4: Within 3 of blue
    # Detail 5: Within 3 of white
# Type 3: Terrain
    # Detail 1: Within 1 of Water
    # Detail 2: Within 1 of Mountain
    # Detail 3: Within 1 of Forest
    # Detail 4: Within 1 of Swamp
    # Detail 5: Within 1 of Desert
    # Detail 6: Forest/Desert
    # Detail 7: Forest/Water
    # Detail 8: Forest/Swamp
    # Detail 9: Forest/Mountain
    # Detail 10: Desert/Water
    # Detail 11: Desert/Swamp
    # Detail 12: Desert/Mountain
    # Detail 13: Water/Swamp
    # Detail 14: Water/Mountain
    # Detail 15: Swamp/Mountain


class Clue:
    def __init__(self):
        self.isTerrainOn = None
        self.isTerrainWithin = None
        self.isStructure = None
        self.isAnimal = None
        self.isColor = None
        self.isWithin = None
