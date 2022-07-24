import map
import clue

test_map = map.Map()

while test_map.main_loop():
    test_map.draw()


"""
Algo notes:

When comparing search location to clue, the clue attribute must first be selected
Use strings (i.e. "bear", "standing stone", "green", "mountain")

After which the target distance amongst all surrounding clues must be checked
(i.e. "bear" within two spaces, "animal" within one)

If all clues agree, that is the spot
Can probably do that with a confirmation of all Clue.doesMatch == true

"""


"""

Pseudocode:

def doesLocationMatchClue(self)

    # Idea that the Clue string equals the Player.location string
    if self.Clue.isTerrainOn == self.location.<> # within 0
        <tile>.doesMatch = True
    elif self.Clue.isTerrainWithin == self.location.<> # within 1
        <tile>.doesMatch = True
    elif self.Clue.isStructure == self.location.<> # within 2
        <tile>.doesMatch = True
    elif self.Clue.isAnimal == self.location.<> # within 2 or 1
        <tile>.doesMatch = True
    elif self.Clue.isColor == self.location.<> # within 3
        <tile>.doesMatch = True
    else <tile>.doesMatch = False

def howManyMatches(self)
    matchCount = 0
    <for/while loop across the entirety of the tiles>
        if <tile>.doesMatch == True
            matchCount += 1

    <for loop end>
"""

ClueArray = []

Clue_Alpha = clue.Clue()
Clue_Alpha.isTerrainOn = "Desert/Mountain";
ClueArray.append(Clue_Alpha)

Clue_Beta = clue.Clue()
Clue_Beta.isTerrainWithin = "Desert"
ClueArray.append(Clue_Beta)

Clue_Gamma = clue.Clue()
Clue_Gamma.isTerrainWithin = "Water"
ClueArray.append(Clue_Gamma)

Clue_Delta = clue.Clue()
Clue_Delta.isTerrainWithin = "Mountain"
ClueArray.append(Clue_Delta)

Clue_Epsilon = clue.Clue()
Clue_Epsilon.isTerrainWithin = "Forest"
ClueArray.append(Clue_Epsilon)

for i in range(-6, 7):
    for j in range(-5, 5):
        for c in ClueArray:
            if c.isTerrainOn is not None:
                print("TO")
            elif c.isTerrainWithin is not None:
                print("TW")
            elif c.isStructure is not None:
                print("S")
            elif c.isAnimal is not None:
                print("A")
            elif c.isColor is not None:
                print("C")
            else:
                print("N")
            #<tile>.doesMatch = False


test_map.quit_app()
