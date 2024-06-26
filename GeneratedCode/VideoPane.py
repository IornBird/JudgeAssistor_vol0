# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.media

from Animator import *

###########################################################################
## Class VideoPane
###########################################################################

class VideoPane ( wx.Panel ):

	def __init__( self, parent ):
		self.setPrivateMembers()
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL )
		
		vidoeSizer = wx.BoxSizer( wx.VERTICAL )
		
		self.stream = wx.media.MediaCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize)
		self.stream.Load( self.videos[1] )
		self.stream.SetPlaybackRate(1)
		self.stream.SetVolume(1)
		# self.stream.ShowPlayerControls()
		vidoeSizer.Add( self.stream, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.timeSlider = wx.Slider( self, wx.ID_ANY, 0, 0, 100, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL )
		vidoeSizer.Add( self.timeSlider, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.PlayPanel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.PlayPanel.SetBackgroundColour( wx.Colour( 192, 192, 192 ) )
		
		playSizer = wx.BoxSizer( wx.HORIZONTAL )
		
		self.playBar = wx.ToolBar( self.PlayPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL ) 
		self.playBar.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, False, wx.EmptyString ) )
		
		self.playButtom = self.playBar.AddTool( wx.ID_ANY, u"tool", wx.Bitmap( u"GeneratedCode\\playButtom.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None )

		self.playBar.Realize()

		playSizer.Add( self.playBar, 0, wx.EXPAND, 5 )
		
		self.timeLabel = wx.StaticText( self.PlayPanel, wx.ID_ANY, u"0:00.00 / -0:00.00", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.timeLabel.Wrap( -1 )
		self.timeLabel.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, False, "Consolas" ) )
		
		playSizer.Add( self.timeLabel, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, 5 )
		
		self.cameraSet = wx.Panel( self.PlayPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		cameraSizer = wx.BoxSizer( wx.HORIZONTAL )
		
		self.cameraText = wx.StaticText( self.cameraSet, wx.ID_ANY, u"Camera", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.cameraText.Wrap( -1 )
		cameraSizer.Add( self.cameraText, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.cameraNum = wx.SpinCtrl( self.cameraSet, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS
									  , 0, len(self.videos), 1 )
		cameraSizer.Add( self.cameraNum, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		self.cameraSet.SetSizer( cameraSizer )
		self.cameraSet.Layout()
		cameraSizer.Fit( self.cameraSet )
		playSizer.Add( self.cameraSet, 1, wx.EXPAND|wx.ALL, 0 )
		
		
		self.PlayPanel.SetSizer( playSizer )
		self.PlayPanel.Layout()
		playSizer.Fit( self.PlayPanel )
		vidoeSizer.Add( self.PlayPanel, 0, wx.EXPAND |wx.ALL, 0 )
		
		
		self.SetSizer( vidoeSizer )
		self.Layout()
		
		# Connect Events
		self.Bind( wx.EVT_TOOL, self.OnPlay, id = self.playButtom.GetId() )
		self.Bind(wx.EVT_SCROLL_THUMBTRACK, self.OnSlide, self.timeSlider)
		self.Bind(wx.EVT_SCROLL_THUMBRELEASE, self.OnSlideEnd, self.timeSlider)
		self.cameraNum.Bind( wx.EVT_SPINCTRL, self.OnChangeCma )

		# setTimers
		addMainAniVal(
			AniVal(func=lambda sender, tNorm, value: [
				self.setTimer()
			])
		)

	def setPrivateMembers(self):
		self.playing = False
		self.isSliding = False
		self.videos = [None,  # first element must be null since it's counted from 1
					   "C:\\Users\\User\\Downloads\\explaning.mp4",
					   "C:\\Users\\User\\Desktop\\source\\桂格超大便當.mp4",
					   "C:\\Users\\User\\Desktop\\source\\source2\\Miyabi_Love_You.mp4"
					   ]
		self.cameraNo = 1

	def __del__( self ):
		pass

	def OnPlay( self, event ):
		self.playing = (self.stream.GetState() == wx.media.MEDIASTATE_PLAYING)
		self.timeSlider.SetMax(self.getVideoLength())
		if self.playing:
			self.stream.Pause()
		else:
			self.stream.Play()

	def OnChangeCma( self, event ):
		self.stream.Pause()
		self.cameraNo = self.cameraNum.GetValue()
		if self.cameraNo == len(self.videos):
			self.cameraNo = 1
			self.cameraNum.SetValue(self.cameraNo)
		elif self.cameraNo == 0:
			self.cameraNo = len(self.videos) - 1
			self.cameraNum.SetValue(self.cameraNo)

		self.stream.Load(self.videos[self.cameraNo])
		if not self.playing:
			self.stream.Play()

	def OnSlideEnd(self, evt):
		position = self.timeSlider.GetValue()
		self.stream.Seek(position)
		self.isSliding = False

	def OnSlide(self, evt):
		self.isSliding = True

	def getPlayingTime(self):
		return self.stream.Tell()

	def getVideoLength(self):
		return self.stream.Length()

	def setTimer(self):
		if not self.isSliding:
			now = self.stream.Tell()
			length = self.stream.Length()
			self.timeLabel.SetLabelText(getTimeFormate(now, length))
			self.timeSlider.SetValue(self.stream.Tell())

# m: ss.ss
def getTimeFormate(now, length):
	length -= now
	T = [[now // 60000, now // 10], [length // 60000, length // 10]]
	S = []
	for c in T:
		s = str(c[0])
		s2 = str(c[1] / 100)
		if c[1] < 1000:
			s2 = '0' + s2
		S.append(s + ':' + s2)
	return S[0] + " / -" + S[1]

