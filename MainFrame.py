import wx
import threading

from GeneratedCode.VideoPane import VideoPane
from TimeLine import TimeLine
from LoopAnimate import *


class MainFrame(wx.Frame):
    def __init__(self, title: str, size):
        super().__init__(parent=None, id=wx.ID_ANY, title=title, size=size)
        self.mutex = threading.Lock()
        self.processing = False
        self.closeReq = False
        # place elements here
        MainTimer[0] = ConstAnimate()
        self.CreateControls()
        MainTimer[0].setAniValues(MainAniVals)
        MainTimer[0].start()
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    # private
    def CreateControls(self):
        hrSpliter = wx.SplitterWindow(self, style=wx.SP_BORDER | wx.SP_LIVE_UPDATE)
        if True:  # set detail for hrSpliter
            vtSpliter = wx.SplitterWindow(hrSpliter, style=wx.SP_BORDER | wx.SP_LIVE_UPDATE)
            if True:  # set detail for vtSpliter
                techList = TimeLine(vtSpliter, wx.VERTICAL)
                videoPane = VideoPane(vtSpliter)
                vtSpliter.SetSashGravity(0.4)
                vtSpliter.SplitVertically(techList, videoPane)
            timeLine = TimeLine(hrSpliter)
            addMainAniVal(
                AniVal(func=lambda sender, tNorm, value: [
                    timeLine.SetScrollRange(
                        videoPane.getVideoLength(), 5000, -1
                    ) if videoPane.getVideoLength() != 0 else None
                ])
            )

            hrSpliter.SetSashGravity(0.7)
            hrSpliter.SplitHorizontally(vtSpliter, timeLine)
        return

    def DoBackgroundProcess(self):
        wx.CallAfter(self.BGProcess)

    def BGProcess(self):
        self.mutex.acquire()
        try:
            if not self.processing: return
            # all GUI changes must be in main thread
        except:
            pass
        self.mutex.release()

    """
    how events handled, and call algorithms in event handler
	examples:
    def OnButtonClicked(self, evt):
        if self.processing: return
        bck = threading.Thread(target=self.buttonJob)
        bck.start()
        bck.join()

    def buttonJob(self):
        if self.processing: return
        self.processing = True
        try:
            # code that ran in another thread
            pass
        except:
            pass
        self.processing = False
    """

    def OnClose(self, closeEvt):
        if self.processing:
            closeEvt.Veto()
            self.closeReq = True
        else:
            if isinstance(MainTimer[0], Animator):
                MainTimer[0].stop()
            self.Destroy()

    def loadFile(self, mess="OpenFile") -> str:
        fd = wx.FileDialog(self, mess, "", "", "All files(*.*)|*.*"
                           , wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if fd.ShowModal() == wx.CANCEL:
            return ""
        return fd.GetPath()

    def saveFile(self, mess="Save as") -> str:
        fd = wx.FileDialog(self, mess, "", "", "All files(*.*)|*.*"
                           , wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if fd.ShowModal() == wx.CANCEL:
            return ""
        return fd.GetPath()
