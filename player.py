class Player(Map):
    def __init__(self):
        self.location = None
        self.color = None
        self.Clue = None

    def doesLocationMatchClue(self)

        # Idea that the Clue string equals the Player.location string
        if self.Clue.isTerrainOn == self.location.<> # within 0
            self.Clue.doesMatch = True
        elif self.Clue.isTerrainWithin == self.location.<> # within 1
            self.Clue.doesMatch = True
        elif self.Clue.isStructure == self.location.<> # within 2
            self.Clue.doesMatch = True
        elif self.Clue.isAnimal == self.location.<> # within 2 or 1
            self.Clue.doesMatch = True
        elif self.Clue.isColor == self.location.<> # within 3
            self.Clue.doesMatch = True
        else self.Clue.doesMatch = False
