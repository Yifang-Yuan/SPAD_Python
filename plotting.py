#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  4 15:48:22 2022

@author: kurtulus
"""

import numpy as np
import pyqtgraph as pg
from datetime import datetime
from pyqtgraph.Qt import QtGui, QtCore, QtWidgets

from config import history_dur

#from GUI.config import history_dur, triggered_dur

class Analog_plot(QtGui.QWidget):

    def __init__(self, parent=None):
        super(QtGui.QWidget, self).__init__(parent)

        # Create axis
        self.axis = pg.PlotWidget(title="Analog signal" , labels={'left':'Volts'})
        self.legend = self.axis.addLegend(offset=(10, 10))
        self.plot_1  = self.axis.plot(pen=pg.mkPen('g'), name='analog 1'  )
        self.plot_2  = self.axis.plot(pen=pg.mkPen('r'), name='analog 2')
        self.axis.setYRange(0, 3.3, padding=0)
        self.axis.setXRange( -history_dur, history_dur*0.02, padding=0)

        # Create controls
        self.demean_checkbox = QtWidgets.QCheckBox('De-mean plotted signals')
        #self.demean_checkbox.stateChanged.connect(self.enable_disable_demean_mode)
        self.offset_label = QtGui.QLabel('Offset channels (mV):')
        self.offset_spinbox = QtGui.QSpinBox()
        self.offset_spinbox.setSingleStep(10)
        self.offset_spinbox.setMaximum(500)
        self.offset_spinbox.setFixedWidth(50)
        #self.enable_disable_demean_mode()
        self.controls_layout = QtGui.QHBoxLayout()
        self.controls_layout.addWidget(self.demean_checkbox)
        self.controls_layout.addWidget(self.offset_label)
        self.controls_layout.addWidget(self.offset_spinbox)
        self.controls_layout.addStretch()

        # Main layout
        self.vertical_layout = QtGui.QVBoxLayout()
        self.vertical_layout.addLayout(self.controls_layout)
        self.vertical_layout.addWidget(self.axis)
        self.setLayout(self.vertical_layout)