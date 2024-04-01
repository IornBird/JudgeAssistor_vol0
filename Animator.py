import wx
import time

"""
usage:
animator = Animator()
aniVals = list[AniVal]()
def setUpAnimations(aniVals):
    aniVals = [
        AniVal(begin, end, lambda sender, tNorm, value: [
            function call
                begin / end is the value desired when
                    the animation begins / ends
                value is used for setting data in specified member,
                    depends on time
            example:
            item.setPostition(f(value))
            self.Refresh()
        ]
    ]
    animator.setAniValues(aniVals)
    animator.setOnIter(self.Refresh)
    animator.setOnStop()

setUpAnimations(aniVals)
element.Bind(wx_EVT, lambda evt: (
    other function call,
    function in Animator
))

animator.reset()

"""

now_ms = lambda: time.time_ns() // 10 ** 6


class Animator(wx.EvtHandler):
    def __init__(self):
        super().__init__()
        self.setPrivateMember()
        self.timer.SetOwner(self)
        self.Bind(wx.EVT_TIMER, self.onTimer)

    def __del__(self):
        self.stop()

    def setPrivateMember(self):
        self.timer = wx.Timer()
        self.aniValues = list[AniVal]()
        self.onIter = lambda: None
        self.onStop = lambda: None
        self.startTime = 0.0
        self.pauseTime = 0.0
        self.duration = 0.0

    def setAniValues(self, values):
        if type(values) == type(self.aniValues):
            self.aniValues = values
        else:
            raise TypeError("values must be list of class AniVal.")

    def getAniValues(self):
        return self.aniValues

    def SetOnIter(self, func):
        self.onIter = func

    def SetOnStop(self, func):
        self.onStop = func

    # if restart is False, durationMs will be ignored
    def start(self, durationMs, restart=True):
        if durationMs <= 0:
            raise RuntimeError("Duration must be positive.")
        if len(self.aniValues) == 0:
            raise RuntimeError("No animate values.")
        if restart:
            self.startTime = now_ms()
            self.duration = durationMs
        else:
            self.startTime += now_ms() - self.pauseTime
        self.timer.Start(10)
        self.pauseTime = -1

    def stop(self):
        if self.isRunning():
            self.pauseTime = now_ms()
        self.timer.Stop()
        self.onStop()

    def setValue(self, setMs):
        if not(0 <= setMs <= self.duration):
            raise RuntimeError("arg setMs must be in [0, duration].")
        if self.isRunning():
            self.startTime = now_ms() - setMs
        else:
            self.startTime = self.pauseTime - setMs

    def reset(self):
        for c in self.aniValues:
            c.OnValueChanged(c, 0, c.startVal)

    def isRunning(self):
        return self.timer.IsRunning()

# private
    def onTimer(self, evt):
        elapsed = now_ms() - self.startTime
        if elapsed >= self.duration:
            self.stop()
            return
        tNorm = elapsed / self.duration
        for c in self.aniValues:
            callback = c.startVal + (c.endVal - c.startVal) * tNorm
            c.OnValueChanged(c, tNorm, callback)
        self.onIter()


class AniVal:
    def __init__(self, startVal=0.0, endVal=0.0, func=lambda sender, tNorm, value: None):
        self.startVal = startVal
        self.endVal = endVal
        self.OnValueChanged = func


MainTimer = [None]  # will be Animator() after wxApp built
MainAniVals = list[AniVal]()  # add Vals in various pane
def addMainAniVal(v: AniVal)-> int:
    MainAniVals.append(v)
    return len(MainAniVals) - 1
