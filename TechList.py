import wx


def toInts(t):
    return tuple(round(c) for c in t)


class TechList(wx.Window):
    def __init__(self, parent, isHorizitional):
        super().__init__(parent, style=wx.FULL_REPAINT_ON_RESIZE)
        self.SetPrivateMembers()
        self.SetBackgroundColour(wx.WHITE)
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.Bind(wx.EVT_PAINT, self.OnPaint, self)
        self.isH = isHorizitional

    def SetPrivateMembers(self):
        self.showBeg = 0
        self.showLen = 10 * 1000
        self.wholeLen = 1
        self.blocks = []
        self.font = None

    def setBlocks(self, blocks):
        self.blocks = blocks

    def setSize(self, beg, showLen, wholeLen):
        self.showBeg = beg
        self.showLen = showLen
        self.wholeLen = wholeLen

    def setBeg(self, beg):
        self.showBeg = beg

    # private
    def OnPaint(self, evt):
        if self.wholeLen == 0:
            return
        dc = wx.PaintDC(self)
        dc.Clear()
        textTop = self.setFont(dc)
        for c in self.blocks:
            dc.SetBrush(wx.Brush(wx.Colour(127, 127, 255)))
            rect = self.setRect(c)
            dc.DrawRectangle(*rect)
            dc.SetTextForeground(wx.BLACK)
            dc.DrawText(self.getCMess(c, dc, rect[2]),
                        *toInts((rect[0], textTop)))

    def setRect(self, c):
        size = self.GetSize()
        length = c.end - c.begin
        return toInts((
            (c.begin - self.showBeg) * size[0] / self.showLen,
            size[1] * 0.1,
            length * size[0] / self.showLen,
            size[1] * 0.8
        ))

    def getCMess(self, c, dc, cmp):
        sSize = dc.GetTextExtent(c.message)[0]
        if sSize <= cmp:
            return c.message
        ASize = dc.GetTextExtent('A')[0]
        return c.message[:int(cmp / ASize)]

    def setFont(self, dc):
        # 24 on 61 * 0.8 (== 48.8)
        bx, by = self.GetSize()
        r = 24 / 48.8 * by
        f1 = wx.Font(round(r), wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        dc.SetFont(f1)
        tSize = dc.GetTextExtent("j")[1]
        self.font = f1
        return (by - tSize) / 2


class TechBlock:
    def __init__(self, time_begin, time_end, message):
        self.begin = time_begin
        self.end = time_end
        self.message = message
