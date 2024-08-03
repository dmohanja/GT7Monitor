from config import formats, settings
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
        self.value.setMinimumHeight(150)
        self.value.setSegmentStyle(QtWidgets.QLCDNumber.Outline)
        self.value.setSegmentStyle(QtWidgets.QLCDNumber.SegmentStyle.Flat)

        # Define frames for rpm bars
        self.gauge = QtWidgets.QGraphicsScene()
        self.gaugeview = QtWidgets.QGraphicsView()
        self.gaugeview.setScene(self.gauge)
        self.bar_count = 16
        self.max_rpm = 12000.0
        self.bars = []
        for i in range(0,self.bar_count):
            if i >= self.bar_count - 4:
                self.bars.append(self.gauge.addRect((i*10)+(i*2),0,10,20,brush=QtGui.QBrush(QtCore.Qt.red)))
            else:
                self.bars.append(self.gauge.addRect((i*10)+(i*2),0,10,20,brush=QtGui.QBrush(QtCore.Qt.white)))

        # Define grids for group boxes
        self.grid = QtWidgets.QGridLayout()
        self.grid.addWidget(self.gaugeview,0,0)
        self.grid.addWidget(self.value,1,0)
        self.grid.setRowStretch(0,5)
        self.grid.setRowStretch(0,1)

        # Add rpm box to group
        self.box = QtWidgets.QVBoxLayout()
        self.box.addLayout(self.grid)
        self.setLayout(self.box)
    
    def update(self,rpm):
        self.value.display(f'{rpm:6.1f}')

        increment = self.max_rpm / self.bar_count

        for i in range(0,self.bar_count):
            if rpm > i*increment:
                self.bars[i].setVisible(True)
            else:
                self.bars[i].setVisible(False)
        