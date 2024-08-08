from config import settings
from PySide6 import QtCore, QtWidgets, QtGui

class RpmGroup(QtWidgets.QGroupBox):
    def __init__(self):
        super().__init__()

        # Define RPM group box
        self.setTitle("RPM")

        # Define RPM digital display
        self.value = QtWidgets.QLCDNumber()
        self.value.setDigitCount(7)
        self.value.setSmallDecimalPoint(True)
        self.value.setMinimumHeight(50)
        self.value.setSegmentStyle(QtWidgets.QLCDNumber.Outline)
        self.value.setSegmentStyle(QtWidgets.QLCDNumber.SegmentStyle.Flat)
        self.value.setStyleSheet("border-style: none;")

        # Define frames for rpm bars
        self.gauge = QtWidgets.QGraphicsScene()
        self.gauge_view = QtWidgets.QGraphicsView()
        self.gauge_view.setInteractive(False)
        self.gauge_view.setScene(self.gauge)
        self.gauge_view.setStyleSheet("border-style: none; background-color: transparent;")
        self.bar_count = settings.RPM_BAR_COUNT
        self.bars = []
        self.grey_brush = QtGui.QBrush(QtCore.Qt.darkGray)
        self.white_brush = QtGui.QBrush(QtCore.Qt.white)
        self.red_brush = QtGui.QBrush(QtCore.Qt.red)
        bar_width = 160 / settings.RPM_BAR_COUNT
        bar_height = 30
        bar_gap = 2
        for i in range(0,self.bar_count):
            self.bars.append(self.gauge.addRect((i*bar_width)+(i*bar_gap),0,bar_width,bar_height,brush=self.grey_brush))

        # Define grid to place gauge and value
        self.grid = QtWidgets.QGridLayout()
        self.grid.addWidget(self.gauge_view,0,0)
        self.grid.addWidget(self.value,1,0)
        self.grid.setRowStretch(0,5)
        self.grid.setRowStretch(0,1)

        # Add grid to self
        self.setLayout(self.grid)
    
    def update_value(self, rpm):
        self.value.display(f'{rpm:6.1f}')

    def update_gauge(self, rpm, redline, limiter):
        increment = limiter / self.bar_count

        for i in range(0,self.bar_count):
            if i * increment < rpm:
                self.bars[i].setBrush(self.white_brush)
                # Redline displayed a little earlier
                if (i+1) * increment > redline:
                    self.bars[i].setBrush(self.red_brush)
            else:
                self.bars[i].setBrush(self.grey_brush)