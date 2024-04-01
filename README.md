# JudgeAssistor_vol0
It's high coupled Judge Assistor, don't learn from here.

## 函數檢查
影片播放是由 GeneratedCode/VideoPane.py 中`self.stream`(型態：`wx.media.MediaCtrl`)處理。

第119行的`OnChangeCma`是改變攝影機時，會做的行為。

該函數的最後，理論上可以讓影片繼續播放。
