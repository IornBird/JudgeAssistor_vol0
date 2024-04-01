# public
class ScoreToken:
    def __init__(self, tech, toward, timeFr = 0, timeTo = 0):
        # double
        self.timeFr = timeFr
        self.timeTo = timeTo
        # Token
        self.tech = tech
        self.toward = toward
        # bool
        self.invalid = False

    def getMessage(self):
        if self.tech != Gam_jeom:
            return self.tech.name + ' ' + chr(0x2192) + ' ' + self.toward.name
        return "Gam_jeom"

    def getScore(self):
        if self.invalid:
            return 0
        return self.tech.score + self.toward.score

    def setInvalid(self, val=True):
        self.invalid = val

# private
class Token:
    def __init__(self, id: int, name: str, score: int):
        self.id = id
        self.name = name
        self.score = score

    def __eq__(self, e):
        return self.id == e.id


# private
# used technique
Punch = Token(1, "Punch", 1)
Kick = Token(2, "Kick", 2)
T_Kick = Token(3, "T.Kick", 4)
# toward
Trunk = Token(4, "Trunk", 0)
Head = Token(5, "Head", 1)
# violating rule
Gam_jeom = Token(0, "Gem-jeom", 1)

# Types = [Gam_jeom, Punch, Kick, T_Kick, Trunk, Head]
