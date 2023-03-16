

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 13:19:18 2022
@author: kurtulus
"""

import os 
import sys
import traceback
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg

from datetime import datetime

from SPCIMAGERAA import SPCIMAGER
from SPADAnalysis import SPADAnalysis
#from PyQt5.QtWidgets import * 
#from PyQt5.QtGui import *

from plotting import Analog_plot

import numpy as np



class SPAD_GUI(QtGui.QWidget):
    
    def __init__(self, parent = None):
        
        super(QtGui.QWidget, self).__init__(parent)
        self.setWindowTitle('SPAD-Photometry')
        self.setGeometry(100,100,1200,950) #Left, top, width, height
        
        __file__ = 'GUI_main.py'
        self.board = None
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
        self.subject_ID = ''
        #self.recording_time_input = ''
        self.running = False
        self.connected = False
        self.refresh_interval = 1000 # Interval to refresh tasks and ports when not running (ms).
        self.available_ports = None
        self.clipboard = QtGui.QApplication.clipboard() # Used to copy strings to computer clipboard.

        # GUI status groupbox.

        self.status_groupbox = QtGui.QGroupBox('GUI status')

        self.status_text = QtGui.QLineEdit('Not connected')
        self.status_text.setStyleSheet('background-color:rgb(210, 210, 210);')
        self.status_text.setReadOnly(True)
        self.status_text.setFixedWidth(105)

        self.guigroup_layout = QtGui.QHBoxLayout()
        self.guigroup_layout.addWidget(self.status_text)
        self.status_groupbox.setLayout(self.guigroup_layout)  

        # Board groupbox

        self.board_groupbox = QtGui.QGroupBox('Board')

        #self.port_label = QtGui.QLabel("Serial port:")
        #self.port_select = QtGui.QComboBox()
        self.connect_button = QtGui.QPushButton('Connect')
        self.connect_button.setIcon(QtGui.QIcon("GUI/icons/connect.svg"))
        self.connect_button.setFixedWidth(110)

        self.boardgroup_layout = QtGui.QHBoxLayout()
        #self.boardgroup_layout.addWidget(self.port_label)
        #self.boardgroup_layout.addWidget(self.port_select)
        self.boardgroup_layout.addWidget(self.connect_button)
        self.board_groupbox.setLayout(self.boardgroup_layout)

        self.connect_button.clicked.connect(
            lambda: self.disconnect() if self.connected else self.connect())

        # Settings groupbox

        # self.settings_groupbox = QtGui.QGroupBox('Acquisition settings')        

        # self.mode_label = QtGui.QLabel("Mode:")
        # self.mode_select = QtGui.QComboBox()
        # self.mode_select.addItems(['2 colour continuous', '1 colour time div.', '2 colour time div.'])
        # #set_cbox_item(self.mode_select, config.default_acquisition_mode)
        # self.rate_label = QtGui.QLabel('Sampling rate (Hz):')
        # self.rate_text = QtGui.QLineEdit()
        # self.rate_text.setFixedWidth(40)

        # self.settingsgroup_layout = QtGui.QHBoxLayout()
        # self.settingsgroup_layout.addWidget(self.mode_label)
        # self.settingsgroup_layout.addWidget(self.mode_select)
        # self.settingsgroup_layout.addWidget(self.rate_label)
        # self.settingsgroup_layout.addWidget(self.rate_text)
        # self.settings_groupbox.setLayout(self.settingsgroup_layout)

        #self.mode_select.activated[str].connect(self.select_mode)
        #self.rate_text.textChanged.connect(self.rate_text_change)

        # Current groupbox

        # self.current_groupbox = QtGui.QGroupBox('LED current (mA)')

        # self.current_label_1 = QtGui.QLabel('CH1:')
        # self.current_spinbox_1 = QtGui.QSpinBox()
        # self.current_spinbox_1.setFixedWidth(50)

        # self.current_label_2 = QtGui.QLabel('CH2:')
        # self.current_spinbox_2 = QtGui.QSpinBox()  
        # self.current_spinbox_2.setFixedWidth(50)

        # self.currentgroup_layout = QtGui.QHBoxLayout()
        # self.currentgroup_layout.addWidget(self.current_label_1)
        # self.currentgroup_layout.addWidget(self.current_spinbox_1)
        # self.currentgroup_layout.addWidget(self.current_label_2)
        # self.currentgroup_layout.addWidget(self.current_spinbox_2)
        # self.current_groupbox.setLayout(self.currentgroup_layout)

        # self.current_spinbox_1.setRange(0,100)
        # self.current_spinbox_2.setRange(0,100)
        #self.current_spinbox_1.setValue(config.default_LED_current[0])
        #self.current_spinbox_2.setValue(config.default_LED_current[1])

        # File groupbox

        self.file_groupbox = QtGui.QGroupBox('Data file')

        self.data_dir_label = QtGui.QLabel("Data dir:")
        self.data_dir_text = QtGui.QLineEdit(self.data_dir)
        self.data_dir_button = QtGui.QPushButton('')
        self.data_dir_button.setIcon(QtGui.QIcon("GUI/icons/folder.svg"))
        self.data_dir_button.setFixedWidth(30)
        self.subject_label = QtGui.QLabel("File Name:")
        self.subject_text = QtGui.QLineEdit(self.subject_ID)
        self.subject_text.setFixedWidth(80)
        self.subject_text.setMaxLength(12)
        #self.filetype_label = QtGui.QLabel("File type:")
        #self.filetype_select = QtGui.QComboBox()
        #self.filetype_select.addItems(['ppd','csv'])
        #set_cbox_item(self.filetype_select, config.default_filetype)

        self.filegroup_layout = QtGui.QHBoxLayout()
        self.filegroup_layout.addWidget(self.data_dir_label)
        self.filegroup_layout.addWidget(self.data_dir_text)
        self.filegroup_layout.addWidget(self.data_dir_button)
        self.filegroup_layout.addWidget(self.subject_label)
        self.filegroup_layout.addWidget(self.subject_text)
        #self.filegroup_layout.addWidget(self.filetype_label)
        #self.filegroup_layout.addWidget(self.filetype_select)
        self.file_groupbox.setLayout(self.filegroup_layout)

        self.data_dir_text.textChanged.connect(self.test_data_path)
        self.data_dir_button.clicked.connect(self.select_data_dir)
        self.subject_text.textChanged.connect(self.test_data_path)
        
        #parameters groupbox 
        self.parameters_groupbox = QtGui.QGroupBox('Session paramaters')
        
        
        self.block_label = QtGui.QLabel('Blocks: ')
        self.block_input = QtGui.QLineEdit(self)
        self.block_input.setFixedWidth(80)
        
        self.recording_time_label = QtGui.QLabel('Recording Time (block/bitplanes): ')
        self.recording_time_input = QtGui.QLineEdit(self)
        self.recording_time_input.setFixedWidth(80)
        #self.recording_time_input.setMaxLength(12)
        #self.recording_time_input.setAlignment(QtCore.Qt.AlignCenter)
        
        
        
        self.parametersgroup_layout = QtGui.QHBoxLayout()
        self.parametersgroup_layout.addWidget(self.block_label)
        self.parametersgroup_layout.addWidget(self.block_input)       
        self.parametersgroup_layout.addWidget(self.recording_time_label)
        self.parametersgroup_layout.addWidget(self.recording_time_input)
        self.parameters_groupbox.setLayout(self.parametersgroup_layout)
        

        # Acquisition groupbox

        self.acquisition_groupbox = QtGui.QGroupBox('Acquisition')

        self.start_button = QtGui.QPushButton('Start')
        self.start_button.setIcon(QtGui.QIcon("GUI/icons/play.svg"))
        self.record_button = QtGui.QPushButton('Record')
        self.record_button.setIcon(QtGui.QIcon("GUI/icons/record.svg"))
        self.stop_button = QtGui.QPushButton('Stop')
        self.stop_button.setIcon(QtGui.QIcon("GUI/icons/stop.svg"))

        self.acquisitiongroup_layout = QtGui.QHBoxLayout()
        self.acquisitiongroup_layout.addWidget(self.start_button)
        self.acquisitiongroup_layout.addWidget(self.record_button)
        self.acquisitiongroup_layout.addWidget(self.stop_button)
        self.acquisition_groupbox.setLayout(self.acquisitiongroup_layout)

        self.start_button.clicked.connect(self.start)
        self.record_button.clicked.connect(self.record)
        self.stop_button.clicked.connect(self.stop)
        
        
        self.gui_title = QtGui.QLabel('SPAD-Photometry')
        self.gui_title.setAlignment(QtCore.Qt.AlignCenter)
        self.gui_title.setFont(QtGui.QFont('Times', 40))
        
        
        self.title_lab_name = QtGui.QLabel('Developed by Nolan Lab ')
        self.title_lab_name.setAlignment(QtCore.Qt.AlignCenter)
        self.title_lab_name.setFont(QtGui.QFont('Times', 20))
        
        # Plots
        
        
        #self.display_layout = QtGui.QHBoxLayout()
        self.image_region = pg.PlotWidget()
        self.image_region.setXRange(0,320)
        self.image_region.setYRange(0,240)
        #self.display_layout.addWidget(self.image_region)
        self.sensor_image = pg.ImageItem()
        self.image_region.addItem(self.sensor_image)
        self.ROI_plot =  pg.PlotWidget(title="Analog signal" , labels={'left':'Photon Counts'})
        self.ROI_plot.setXRange(0,-1000)
        self.ROI_plot.setYRange(0,10000)
        self.ROI_plot.setFixedWidth(600)
        
        self.legend = self.ROI_plot.addLegend(offset=(10, 10))
        self.plot_1  = self.ROI_plot.plot(pen=pg.mkPen('r'), name='Background Signal'  )
        self.plot_2  = self.ROI_plot.plot(pen=pg.mkPen('g'), name='Original Signal')
        
        self.ROI_region_red = pg.CircleROI([10, 10], [50, 50], pen=pg.mkPen('r', width=4.5))
        self.ROI_region_green = pg.CircleROI([100, 100], [50, 50], pen=pg.mkPen('g', width=4.5))
        self.image_region.addItem(self.ROI_region_red)
        self.image_region.addItem(self.ROI_region_green)
        self.ROI_region_red.setZValue(10)
        self.ROI_region_green.setZValue(10)
        #self.display_layout.addWidget(self.ROI_plot)
        
        

        #self.myplot = pg.PlotWidget(title="Analog signal" , labels={'left':'Photon Counts'})
        #self.myplot.setXRange(0,-1000)
        #self.myplot.setYRange(0,100000)
        #self.legend = self.myplot.addLegend(offset=(10, 10))
        #self.plot_1  = self.myplot.plot(pen=pg.mkPen('g'), name='Background Signal'  )
        #self.plot_2  = self.myplot.plot(pen=pg.mkPen('r'), name='Original Signal')
        #self.analog_plot  = Analog_plot(self)
        #self.digital_plot = Digital_plot()
        #self.event_triggered_plot = Event_triggered_plot()

        #self.record_clock = Record_clock(self.analog_plot.axis)

        # Main layout

        self.vertical_layout     = QtGui.QVBoxLayout()
        self.horizontal_layout_1 = QtGui.QHBoxLayout()
        self.horizontal_layout_2 = QtGui.QHBoxLayout()
        self.horizontal_layout_3 = QtGui.QHBoxLayout()
        self.horizontal_layout_4 = QtGui.QHBoxLayout()
        self.horizontal_layout_5 = QtGui.QHBoxLayout()
        self.horizontal_layout_6 = QtGui.QHBoxLayout()
        self.horizontal_layout_7 = QtGui.QHBoxLayout()
        #self.plot_splitter = QtGui.QSplitter(QtCore.Qt.Vertical)

        

        self.horizontal_layout_1.addWidget(self.image_region)
        self.horizontal_layout_1.addWidget(self.ROI_plot)
        self.horizontal_layout_2.addWidget(self.gui_title)
        self.horizontal_layout_3.addWidget(self.title_lab_name)
        self.horizontal_layout_4.addWidget(self.file_groupbox)
        self.horizontal_layout_5.addWidget(self.status_groupbox)
        self.horizontal_layout_5.addWidget(self.board_groupbox)
        self.horizontal_layout_5.addWidget(self.parameters_groupbox)
        #self.horizontal_layout_1.addWidget(self.settings_groupbox)
        #self.horizontal_layout_1.addWidget(self.current_groupbox)
        self.horizontal_layout_7.addWidget(self.acquisition_groupbox)
        #self.plot_splitter.addWidget(self.analog_plot)
        #self.plot_splitter.addWidget(self.digital_plot.axis)
        #self.plot_splitter.addWidget(self.event_triggered_plot.axis)
        #self.plot_splitter.setSizes([100,60,100])
        #self.vertical_layout.addWidget(self.display_region)


        self.vertical_layout.addLayout(self.horizontal_layout_1)
        self.vertical_layout.addLayout(self.horizontal_layout_2)
        self.vertical_layout.addLayout(self.horizontal_layout_3)
        self.vertical_layout.addLayout(self.horizontal_layout_4)
        self.vertical_layout.addLayout(self.horizontal_layout_5)
        self.vertical_layout.addLayout(self.horizontal_layout_6)
        self.vertical_layout.addLayout(self.horizontal_layout_7)
        
        #self.vertical_layout.addWidget(self.plot_splitter)
        #self.vertical_layout.addWidget(self.myplot)
        
        



        self.setLayout(self.vertical_layout)


        #print('I AM HERE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1')
        self.data1 = np.zeros(1000)
        self.data2 = np.zeros(1000)
        # Setup Timers.


        #self.update_timer = QtCore.QTimer() # Timer to regularly call process_data()
        #self.update_timer.timeout.connect(self.process_data)
        #self.refresh_timer = QtCore.QTimer() # Timer to regularly call refresh() when not running.
        #self.refresh_timer.timeout.connect(self.refresh)

        # Initial setup.

        #self.disconnect() # Set initial state as disconnected.
        #self.refresh()    # Refresh ports list.
        #self.refresh_timer.start(self.refresh_interval) 
        
    def connect(self):
        try:
            #self.board = Acquisition_board(self.port_select.currentText())
            #self.select_mode(self.mode_select.currentText())
            #self.port_select.setEnabled(False)
            #self.settings_groupbox.setEnabled(True)
            #self.current_groupbox.setEnabled(True)
            
            self.sensor = SPCIMAGER('SPCIMAGER_TOP.bit')
            self.sensor.SensorConnect(self.sensor.bank)
            self.file_groupbox.setEnabled(True)
            self.acquisition_groupbox.setEnabled(True)
            self.stop_button.setEnabled(False)
            self.record_button.setEnabled(False)
            self.connect_button.setText('Disconnect')
            self.connect_button.setIcon(QtGui.QIcon("GUI/icons/disconnect.svg"))
            self.status_text.setText('Connected')
            #self.board.set_LED_current(self.current_spinbox_1.value(),self.current_spinbox_2.value())
            #self.current_spinbox_1.valueChanged.connect(
                #lambda v:self.board.set_LED_current(LED_1_current=int(v)))
            #self.current_spinbox_2.valueChanged.connect(
                #lambda v:self.board.set_LED_current(LED_2_current=int(v)))
            #self
            self.connected = True
        #except SerialException:
            #self.status_text.setText('Connection failed')
        #except PyboardError:
            #self.status_text.setText('Connection failed')
            #try:
                #self.board.close()
        except AttributeError:
                pass
        
    def disconnect(self):
        # Disconnect from the sensor.
        #if self.board: self.board.close()
        #self.board = None
        #self.settings_groupbox.setEnabled(False)
        #self.current_groupbox.setEnabled(False)
        self.file_groupbox.setEnabled(False)
        self.acquisition_groupbox.setEnabled(False)
        self.port_select.setEnabled(True)
        self.connect_button.setText('Connect')
        self.connect_button.setIcon(QtGui.QIcon("GUI/icons/connect.svg"))
        self.status_text.setText('Not connected')
        self.connected = False
        self.sensor.SensorDisconnect()
                
        
    def start(self):
        # Reset plots.
        #self.analog_plot.reset(self.board.sampling_rate)
        #self.digital_plot.reset(self.board.sampling_rate)
        #self.event_triggered_plot.reset(self.board.sampling_rate)
        # Start acquisition.
        #self.board.start()
        #self.refresh_timer.stop()
        #self.update_timer.start(config.update_interval)
        
        
        #data1 = data_new.sum()
        #self.curve1 = self.myplot.plot(self.data1)
        
        self.sensor.SensorStart()
        self.running = True
        # Update UI.
        self.board_groupbox.setEnabled(False)
        #self.settings_groupbox.setEnabled(False)
        self.start_button.setEnabled(False)
        #if self.test_data_path():
        self.record_button.setEnabled(True)
        self.stop_button.setEnabled(True)
        self.status_text.setText('Running')
        
        # update all plots

        
        self.timer = QtCore.QTimer()
        self.timer.setInterval(1)
        self.timer.timeout.connect(self.update)
        self.timer.start()
        
        
    def record(self):
        
        print(self.data_dir)
        if os.path.isdir(self.data_dir):
            filetype = '.bin'
            date_time = datetime.now()
            file_name = self.data_dir + "/" + self.subject_ID + date_time.strftime('-%Y-%m-%d-%H%M%S')
            #self.clipboard.setText(file_name)
            self.status_text.setText('Recording')
            #self.current_groupbox.setEnabled(False)
            self.file_groupbox.setEnabled(False)
            self.record_button.setEnabled(False)
            #self.subject_text.setEnabled(False)
            #self.data_dir_text.setEnabled(False)
            #self.data_dir_button.setEnabled(False)
            #self.record_clock.start()
            self.recording_time = int(self.recording_time_input.text())
            self.block_number = int(self.block_input.text())
            print(file_name)
            self.sensor.RecordData(self.recording_time*10000, self.block_number, file_name)
            self.status_text.setText('Recording is done!')
            self.file_groupbox.setEnabled(True)
            self.record_button.setEnabled(True)
            
        else:
            self.data_dir_text.setText('Set valid directory')
            self.data_dir_label.setStyleSheet("color: rgb(255, 0, 0);")

        
    def stop(self):
        #self.board.stop()
        #self.update_timer.stop()
        #self.refresh_timer.start(self.refresh_interval)
        self.sensor.SensorDisconnect()
        self.running = False
        self.stop_button.setEnabled(False)
        #self.board.serial.reset_input_buffer()
        self.board_groupbox.setEnabled(True)
        #self.settings_groupbox.setEnabled(True)
        #self.current_groupbox.setEnabled(True)
        self.file_groupbox.setEnabled(True)
        self.start_button.setEnabled(True)
        self.record_button.setEnabled(False)
        #self.subject_text.setEnabled(True)
        #self.data_dir_text.setEnabled(True)
        #self.data_dir_button.setEnabled(True)
        self.status_text.setText('Connected')
        #self.record_clock.stop()
        self.timer.stop()
        
        
        
    def test_data_path(self):
        # Checks whether data dir and subject ID are valid.
        self.data_dir = self.data_dir_text.text()
        self.subject_ID = self.subject_text.text()
        if (self.running and os.path.isdir(self.data_dir) and str(self.subject_ID)):
                self.record_button.setEnabled(True)
        
    def select_data_dir(self):
        self.data_dir_text.setText(
            QtGui.QFileDialog.getExistingDirectory(self, 'Select data folder', self.data_dir))
        
        
    def update(self):
        print('update is runing')
        global data1, ptr1
        self.data1[:-1] = self.data1[1:]  # shift data in the array one sample left
                                # (see also: np.roll)
        self.data2[:-1] = self.data2[1:]  
        #new_data = np.unpackbits(self.sensor.GetLiveData()).sum()   

        new_data = np.asarray(list(self.sensor.GetLiveData()))
        converted_data = new_data.reshape((-1,4))
        sum_bits = converted_data.sum(axis=1)
        self.image_data = sum_bits.reshape(240,320)
        self.sensor_image.setImage(np.rot90(self.image_data))                  
        #self.data1[-1] =new_data
        #self.x = np.linspace(-1000, 0,1000)
        #self.plot_2.setData(self.x, self.data1)
        
        self.green_signal = self.ROI_region_green.getArrayRegion(self.image_data, self.sensor_image).sum()
        self.red_signal = self.ROI_region_red.getArrayRegion(self.image_data, self.sensor_image).sum()
        
        
        new_data = self.red_signal
        #self.data2[:-1] = self.data2[1:]                   
        self.data1[-1] =new_data
        self.data2[-1] = self.green_signal
        self.x = np.linspace(-1000, 0,1000)
        self.plot_1.setData(self.x, self.data1)
        self.plot_2.setData(self.x, self.data2)
        
        

def launch_GUI():
        '''Launch the GUI.'''
        app = QtGui.QApplication([])  # Start QT
        spad_GUI = SPAD_GUI()
        spad_GUI.show()
        #sys.excepthook = spad_GUI.excepthook
        app.exec_()
