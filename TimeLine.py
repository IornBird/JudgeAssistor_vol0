import wx
from ScoreBar import ScoreBar
from TechList import *
from Animator import *


class TimeLine(wx.Panel):
    def __init__(self, parent, style=wx.HORIZONTAL):
        super().__init__(parent)
        if style == wx.HORIZONTAL:
            Lst = [(c // 2 + 1, c % 2) for c in range(4)]
            SclPlc = [(3, 0), (1, 2)]
            isH = True
        elif style == wx.VERTICAL:
            Lst = [(c % 2, c // 2) for c in range(4)]
            SclPlc = [(0, 2), (2, 1)]
            isH = False
        else:
            raise ValueError("Please specify the arrangement.")
        self.CreateControls(isH, Lst, SclPlc)
        self.Bind(wx.EVT_SCROLL, self.OnScroll, self.scroll)

    def CreateControls(self, isH, Lst, SclPlc):
        self.sizer = wx.GridBagSizer()
        if True:
            self.BlueScore = ScoreBar(self, True)
            self.BlueList = TechList(self, isH)
            self.RedScore = ScoreBar(self, False)
            self.RedList = TechList(self, isH)
        self.scroll = wx.ScrollBar(self, style=
            wx.SB_HORIZONTAL if isH else wx.SB_VERTICAL)

        if isH:
            self.timeSpecifier = wx.Slider(self)
            self.sizer.Add(self.timeSpecifier, (0, 1), (1, 1), wx.EXPAND | wx.ALL)
        self.sizer.Add(self.BlueScore, Lst[0], (1, 1), wx.CENTER | wx.EXPAND | wx.ALL)
        self.sizer.Add(self.BlueList, Lst[1], (1, 1), wx.EXPAND | wx.ALL)
        self.sizer.Add(self.RedScore, Lst[2], (1, 1), wx.CENTER | wx.EXPAND | wx.ALL)
        self.sizer.Add(self.RedList, Lst[3], (1, 1), wx.EXPAND | wx.ALL)
        self.sizer.Add(self.scroll, SclPlc[0], SclPlc[1], wx.EXPAND | wx.ALL)

        if isH:
            self.sizer.AddGrowableRow(1)
            self.sizer.AddGrowableRow(2)
            self.sizer.AddGrowableCol(1)
        else:
            self.sizer.AddGrowableCol(0)
            self.sizer.AddGrowableCol(1)
            self.sizer.AddGrowableRow(1)
        self.sizer.SetMinSize(50, 50)
        self.SetSizerAndFit(self.sizer)

        # demo
        self.BlueList.setBlocks([
            TechBlock(0, 1000, "Abc"),
            TechBlock(2010, 2601, "Laura"),
            TechBlock(3000, 3500, "Akari")
        ])

    def refresh(self):
        self.BlueList.Refresh()
        self.RedList.Refresh()

    def SetScrollRange(self, length, showSize, showBegin=-1):
        if showBegin == -1:
            showBegin = self.scroll.GetThumbPosition()
        self.scroll.SetScrollbar(showBegin, showSize, length, 0)
        self.BlueList.setSize(showBegin, showSize, length)
        self.RedList.setSize(showBegin, showSize, length)

    def OnScroll(self, evt):
        place = self.scroll.GetThumbPosition()
        self.BlueList.setBeg(place)
        self.RedList.setBeg(place)
        self.refresh()
'''
class TimeLine(wx.ScrolledWindow):
    def __init__(self, parent, step):
        super().__init__(parent)
        super().SetScrollRate(step, 0)
        
        
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.scoreBar = ScoreBar(self)
        self.scoreBar.setName("Goku S.", True)
        self.sizer.Add(self.scoreBar, 1, wx.EXPAND)
        self.SetSizerAndFit(self.sizer)
'''


