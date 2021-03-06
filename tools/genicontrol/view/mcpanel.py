﻿#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
##
## Grundfos GENIBus Library for Arduino.
##
## (C) 2007-2013 by Christoph Schueler <github.com/Christoph2,
##                                      cpu12.gems@googlemail.com>
##
##  All Rights Reserved
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License along
## with this program; if not, write to the Free Software Foundation, Inc.,
## 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
##
##

from collections import namedtuple
import wx
from wx.lib.scrolledpanel import ScrolledPanel
import genicontrol.controlids as controlids
from genicontrol.model.config import DataitemConfiguration
import genicontrol.dataitems as dataitems
from genicontrol.view.statuspanel import StatusPanel, AlarmPanel, PumpOperationPanel

ToggleButton = namedtuple('ToggleButton', 'id, labelOn, labelOff attrName')

def createToggleButton(parent, buttonDesc, sizer):
    btn = wx.ToggleButton(parent, label = buttonDesc.labelOn, id = buttonDesc.id)
    btn.labelOn = buttonDesc.labelOn
    btn.labelOff = buttonDesc.labelOff
    btn.bgColor = btn.GetBackgroundColour()
    sizer.Add(btn, 1, wx.ALL, 5)
    setattr(parent, buttonDesc.attrName, btn)
    btn.Bind(wx.EVT_TOGGLEBUTTON, parent.toggledbutton)
    return btn

class Controls(wx.Panel):
    def __init__(self, parent):
        self.toggleButtons = (
            ToggleButton(controlids.ID_CMD_REMOTE_LOCAL, 'Remote', 'Local', 'btnRemoteLocal'),
            ToggleButton(controlids.ID_CMD_START_STOP, 'Start', 'Stop', 'btnStartStop'),
        )
        wx.Panel.__init__(self, parent = parent, id = wx.ID_ANY)
        sizer1 = wx.BoxSizer(wx.VERTICAL)

        sizer3 = wx.BoxSizer(wx.HORIZONTAL)

        sizer3.Add(wx.StaticText(self, -1, ''), 1, wx.ALL, 5)
        self.btnRefUp = wx.Button(self, label = '+', id = controlids.ID_CMD_REF_UP)
        sizer3.Add(self.btnRefUp, 1, wx.ALL | wx.GROW, 5)
        self.btnRefDown = wx.Button(self, label = '-', id = controlids.ID_CMD_REF_DOWN)
        sizer3.Add(self.btnRefDown, 1, wx.ALL | wx.GROW, 5)
        sizer1.Add(sizer3)#, 1, wx.ALL, 5)

        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        for btn in self.toggleButtons:
            createToggleButton(self, btn, sizer2)

        btn = wx.Button(self, label = 'Min', id = controlids.ID_CMD_MIN)
        sizer2.Add(btn, 1, wx.ALL, 5)
        btn = wx.Button(self, label = 'Max', id = controlids.ID_CMD_MAX)
        sizer2.Add(btn, 1, wx.ALL, 5)

        sizer1.Add(sizer2)

        self.SetSizerAndFit(sizer1)

        self.enableControls((controlids.ID_CMD_MAX, controlids.ID_CMD_MIN))

    def toggledbutton(self, event):
        # Active State
        if event.EventObject.GetValue() == True:
            event.EventObject.SetLabel(event.EventObject.labelOff)
            event.EventObject.SetBackgroundColour(wx.Color(0, 255, 0))
        # Inactive State
        if event.EventObject.GetValue() == False:
            event.EventObject.SetLabel(event.EventObject.labelOn)
            event.EventObject.SetBackgroundColour(event.EventObject.bgColor)

    def setRemoteMode(self):
        pass

    def setLocalMode(self):
        pass

    def setStartMode(self):
        pass

    def setStopMode(self):
        pass

    def enableControls(self, controlIDs):
        for controlID in controlIDs:
            control = self.FindWindowById(controlID)
            control.Enable(True)

    def disableControls(self, controlIDs):
        for controlID in controlIDs:
            control = self.FindWindowById(controlID)
            control.Enable(False)

class MCPanel(ScrolledPanel):
    def __init__(self, parent):
        ScrolledPanel.__init__(self, parent = parent, id = wx.ID_ANY)

        sizer = wx.FlexGridSizer(rows = 2, cols = 3, hgap = 5, vgap = 5)
##
##        sizer.AddGrowableRow(0, 1)
##        sizer.AddGrowableRow(1, 1)
##        sizer.AddGrowableCol(0, 1)
##        sizer.AddGrowableCol(1, 1)
##
        #sizer.SetFlexibleDirection(wx.BOTH)
        self.statusPanel = StatusPanel(self)
        sizer.Add(self.statusPanel, 1, wx.ALIGN_LEFT | wx.ALIGN_TOP | wx.EXPAND, 5)
        self.pumpOperationPanel = PumpOperationPanel(self)
        sizer.Add(self.pumpOperationPanel, 1, wx.ALIGN_RIGHT | wx.ALIGN_TOP | wx.EXPAND | wx.ALL, 5)
        self.alarmPanel = AlarmPanel(self)
        sizer.Add(self.alarmPanel, 1, wx.ALIGN_RIGHT | wx.ALIGN_TOP | wx.EXPAND | wx.ALL, 5)
        self.controlsPanel = Controls(self)
        sizer.Add(self.controlsPanel, 1, wx.ALIGN_LEFT | wx.ALIGN_BOTTOM | wx.EXPAND, 5)

        self.SetSizerAndFit(sizer)
        self.SetupScrolling()
        sizer.Layout()

    def setLEDState(self, num ,on):
        self.statusPanel.ledControl.setState(num, on)

    def getLEDState(self, num):
        return self.statusPanel.ledControl.getState(num)
