import wx
from ScoreToken import *


def toInts(t):
    return tuple(round(c) for c in t)

class ScoreBar(wx.Panel):
    def __init__(self, parent, isBlue):
        super().__init__(parent, style=wx.FULL_REPAINT_ON_RESIZE)
        self.score = 0
        self.violate = 0
        self.name = ""
        self.isBlue = isBlue
        self.CreateControls()
        # self.setPrivateMembers()

    def CreateControls(self):
        scoreFont = wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.SetFont(scoreFont)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        if True:
            self.scorePane = ScorePane(self, self.isBlue)
            self.namePane = wx.StaticText(self, label="Goku S.")
        self.sizer.Add(self.scorePane, 2, wx.EXPAND | wx.ALL)
        self.sizer.Add(self.namePane, 3, wx.CENTER)
        self.SetSizerAndFit(self.sizer)

    def setName(self, name, isBlue):
        self.name = name
        self.isBlue = isBlue
        # self.scorePane.SetBackgroundColour(wx.BLUE if self.isBlue else wx.RED)
        self.namePane.SetLabelText(name)

    def setScore(self, score=None, violate=None):
        if score != None:
            self.score = score
        if violate != None:
            self.violate = violate
        self.scorePane.setScores(score, violate)


# private
class ScorePane(wx.Panel):
    def __init__(self, parent, isBlue):
        super().__init__(parent, style=wx.FULL_REPAINT_ON_RESIZE)
        self.score = 0
        self.violate = 0
        self.isBlue = isBlue
        self.setPrivateMembers()
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.Bind(wx.EVT_PAINT, self.OnPaint, self)

    def setScores(self, score, violate):
        self.score = score
        self.violate = violate

    def setPrivateMembers(self):
        self.corner = (0, 0)
        self.blockSize = 0

    def OnPaint(self, evt):
        dc = wx.AutoBufferedPaintDC(self)
        dc.Clear()
        gc = wx.GraphicsContext.Create(dc)
        if gc:
            self.setCorner()
            corner2 = (
                self.corner[0] + self.blockSize,
                self.corner[1] + self.blockSize * 0.15
            )
            gc.SetBrush(wx.Brush(wx.BLUE if self.isBlue else wx.RED))
            gc.DrawRectangle(*self.corner, self.blockSize, self.blockSize)
            gc.SetBrush(wx.Brush(wx.WHITE))
            size = self.blockSize * 0.7
            gc.DrawRectangle(
                *corner2,
                size, size
            )

            fonts = self.setTextCorner(gc, corner2)
            gc.SetFont(fonts[0][0], wx.WHITE)
            gc.DrawText(str(self.score), *fonts[0][1])
            gc.SetFont(fonts[1][0], wx.BLACK)
            gc.DrawText(str(self.violate), *fonts[1][1])

    def setCorner(self):
        bx, by = self.GetSize()
        rx, ry = bx / 1.7, by
        if rx > ry:
            self.blockSize = ry * 0.9
            self.corner = (
                (bx - self.blockSize * 1.7) / 2, by * 0.05
            )
        else:
            self.blockSize = rx * 0.9
            self.corner = (
                bx * 0.05, (by - self.blockSize) / 2
            )

    def setTextCorner(self, gc, corner2):
        # 36 / 24 on 61 * 0.9 (== 54.9)
        r = 12 / 54.9 * self.blockSize
        f1 = wx.Font(round(3 * r), wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        f2 = wx.Font(round(2 * r), wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        size, size2 = self.blockSize, self.blockSize * 0.7

        gc.SetFont(f1, wx.WHITE)
        tSize = gc.GetTextExtent(f"{self.score}")

        textCorner = [
            (self.corner[0] + (size - tSize[0]) / 2, self.corner[1] + (size - tSize[1]) / 2),
            (corner2[0] + (size - tSize[0]) * 0.7 / 2, corner2[1] + (size - tSize[1]) * 0.7 / 2)
        ]
        return [
            [f1, toInts(textCorner[0])],
            [f2, toInts(textCorner[1])]
        ]

