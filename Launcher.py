from MainFrame import *

if __name__ == '__main__':
    app = wx.App()
    frame = MainFrame("Title", (1024, 576))
    frame.Show()
    app.MainLoop()
