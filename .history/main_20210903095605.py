################################################################################
##
## BY: PHUNG HUNG BINH
## PROJECT MADE WITH: QtPy5 Designer
## Ver: 1.0.0
##
## There are limitations on Qt licenses if you want to use your products
## commercially, I recommend reading them on the official website:
## https://doc.qt.io/qtforpython/licenses.html
##
################################################################################

import sys
import matplotlib
from matplotlib import cm
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.ticker as ticker
from matplotlib.animation import FuncAnimation
import numpy as np
import platform
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from app_modules import *

class plot_main(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.patch.set_facecolor('#343b48')
        fig.suptitle('Robot-Controller Simulation Flatform',color='white',fontsize=15)
        matplotlib.style.use("seaborn-notebook")

        self.axes = fig.gca(projection='3d')
        self.axes.set_facecolor('#343b48')
        self.axes.set_xlim(10,-45)
        self.axes.set_ylim(-35, 35)
        self.axes.set_zlim(-5, 35)

        self.axes.set_xlabel('X_axis',color='white',fontsize=10)
        self.axes.set_ylabel('Y_axis',color='white',fontsize=10)
        self.axes.set_zlabel('Z_axis',color='white',fontsize=10)
        self.axes.tick_params(axis='x', colors='white')
        self.axes.tick_params(axis='y', colors='white')
        self.axes.tick_params(axis='z', colors='white')
        super(plot_main, self).__init__(fig)
        fig.tight_layout()

class plot_camera(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.patch.set_facecolor('#343b48')
        fig.tight_layout()
        fig.suptitle('Camera Zooming',color='white',fontsize=15)
        matplotlib.style.use("seaborn-notebook")
        self.axes = fig.gca(projection='3d')
        self.axes.set_facecolor('#343b48')
        self.axes.set_xlim(0,-45)
        self.axes.set_ylim(-35,0)
        self.axes.set_zlim(0,10)
        self.axes.set_xlabel('X_axis',color='white',fontsize=10)
        self.axes.set_ylabel('Y_axis',color='white',fontsize=10)
        self.axes.set_zlabel('Z_axis',color='white',fontsize=10)
        self.axes.tick_params(axis='x', colors='white')
        self.axes.tick_params(axis='y', colors='white')
        self.axes.tick_params(axis='z', colors='white')
        super(plot_camera, self).__init__(fig)
        fig.tight_layout()

class plot_analysis(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.patch.set_facecolor('#343b48')
        fig.tight_layout()
        matplotlib.style.use("seaborn-notebook")
        self.axes = fig.add_subplot(111)
        self.axes.grid(True)
        self.axes.xaxis.set_ticklabels([])
        self.axes.tick_params(axis='y', colors='white')
        super(plot_analysis, self).__init__(fig)
        #fig.tight_layout()

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = uic.loadUi('robot_control_GUI_ver1.ui',self)

        ## Check operation system version: Window,Linux...
        print('System: ' + platform.system())
        print('Version: ' +platform.release())


        ## Title Bar and size of Windown Settings:
        UIFunctions.removeTitleBar(True)
        self.setWindowTitle('Robotics Controller Resource - Python 3.8.10')
        UIFunctions.labelTitle(self, 'Robotics Controller Resource - Python 3.8.10')
        UIFunctions.labelDescription(self, 'put description here')
        startSize = QSize(1000, 720)
        self.resize(startSize)
        self.setMinimumSize(startSize)

        ## ==> LOAD DEFINITIONS ##
        ########################################################################
        UIFunctions.uiDefinitions(self)
        ## ==> Create Menus ##
        ########################################################################

        ## Toggle menu ##
        self.ui.btn_toggle_menu.clicked.connect(lambda: UIFunctions.toggleMenu(self, 220, True))

        ## START MENU => SELECTION
        UIFunctions.selectStandardMenu(self, "btn_Home")

        ## First page to appear when the API first circle ##
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)

        ## USER ICON ==> SHOW HIDE ##
        UIFunctions.userIcon(self, "PHB", "", True)

        ## ACTIVATION BUTTON TO CHANGE MENUS:
        self.btn_Chart.clicked.connect(self.Button)
        self.btn_Home.clicked.connect(self.Button)
        self.btn_Manual.clicked.connect(self.Button)
        self.btn_Visualize.clicked.connect(self.Button)
        self.btn_settings.clicked.connect(self.Button)
        self.btn_camera.clicked.connect(lambda: UIFunctions.setup_camera(self))

        ## setting 3D-PLOTTING IN MATPLOTLIB:
        self.canvas = plot_main(self, width=50, height=50, dpi=70)
        self.canvas_camera = plot_camera(self, width=50, height=50, dpi=70)
        self.canvas_data = plot_analysis(self, width=5, height=4, dpi=70)
        self.ui.formLayout.addWidget(self.canvas)
        self.ui.formLayout_4.addWidget(self.canvas_camera)
        self.ui.formLayout_12.addWidget(self.canvas_data)
        self.reference_plot = None
        ## ==> MOVE WINDOW FUNCTIONALITY ##
        ########################################################################
        def moveWindow(event):

        ## moving window ##
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()

        self.ui.frame_label_top_btns.mouseMoveEvent = moveWindow


        ## SHOW ==> MAIN WINDOW
        ########################################################################
        self.show()

    def Button(self):
        # GET BT CLICKED
        btnWidget = self.sender()

        # PAGE HOME
        if btnWidget.objectName() == "btn_Home":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
            UIFunctions.resetStyle(self, "btn_Home")
            UIFunctions.labelPage(self, "Home")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))

        # PAGE CHART
        if btnWidget.objectName() == "btn_Chart":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_data)
            UIFunctions.resetStyle(self, "btn_Chart")
            UIFunctions.labelPage(self, "Data Analysis")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))

        # PAGE MANUAL
        if btnWidget.objectName() == "btn_Manual":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_manual)
            UIFunctions.resetStyle(self, "btn_Manual")
            UIFunctions.labelPage(self, "Kinematics")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))

        # PAGE VISUALIZE
        if btnWidget.objectName() == "btn_Visualize":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_visualize)
            UIFunctions.resetStyle(self, "btn_Visualize")
            UIFunctions.labelPage(self, "Visualize")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))

        # PAGE SETTINGS
        if btnWidget.objectName() == "btn_settings":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_setting)
            UIFunctions.labelPage(self, "Custom Widgets")


    ########################################################################

    ## EVENT ==> MOUSE DOUBLE CLICK
    ########################################################################
    def eventFilter(self, watched, event):
        if watched == self.le and event.type() == QtCore.QEvent.MouseButtonDblClick:
            print("pos: ", event.pos())
    ## ==> END ##

    ## EVENT ==> MOUSE CLICK
    ########################################################################
    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()
        if event.buttons() == Qt.LeftButton:
            print('Mouse click: LEFT CLICK')
        if event.buttons() == Qt.RightButton:
            print('Mouse click: RIGHT CLICK')
        if event.buttons() == Qt.MidButton:
            print('Mouse click: MIDDLE BUTTON')

    def keyPressEvent(self, event):
        print('Key: ' + str(event.key()) + ' | Text Press: ' + str(event.text()))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    QtGui.QFontDatabase.addApplicationFont('fonts/segoeui.ttf')
    QtGui.QFontDatabase.addApplicationFont('fonts/segoeuib.ttf')
    window = MainWindow()
    sys.exit(app.exec_())
