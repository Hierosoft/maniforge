#!/usr/bin/env python3
import wx
from maniforge.slicerwx import MainFrame

if __name__ == "__main__":
    app = wx.App()
    frame = MainFrame()
    frame.Show()
    app.MainLoop()
