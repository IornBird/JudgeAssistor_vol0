from Animator import *

class ConstAnimate(Animator):
    def __init__(self):
        super().__init__()

    def start(self, restart=True):
        super().start(1, restart)

# private
    def onTimer(self, evt):
        for c in self.aniValues:
            callback = c.startVal
            c.OnValueChanged(c, 0, callback)
        self.onIter()


class AniVal:
    def __init__(self, startVal=0.0, endVal=0.0, func=lambda sender, tNorm, value: None):
        self.startVal = startVal
        self.endVal = endVal
        self.OnValueChanged = func