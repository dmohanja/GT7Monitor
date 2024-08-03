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
        self.gauge_view = QtWidgets.QGraphicsView()
        self.gauge_view.setScene(self.gauge)
        self.bar_count = settings.RPM_BAR_COUNT
        #self.rpm_max = max
        #self.rpm_redline = redline
        #self.increment = self.rpm_max / self.bar_count
        self.bars = []
        self.white_brush = QtGui.QBrush(QtCore.Qt.white)
        self.red_brush = QtGui.QBrush(QtCore.Qt.red)
        for i in range(0,self.bar_count):
            self.bars.append(self.gauge.addRect((i*20)+(i*2),0,20,20,brush=self.white_brush))
        
        QtWidgets.QGraphicsRectItem()

        # Define grids for group boxes
        self.grid = QtWidgets.QGridLayout()
        self.grid.addWidget(self.gauge_view,0,0)
        self.grid.addWidget(self.value,1,0)
        self.grid.setRowStretch(0,5)
        self.grid.setRowStretch(0,1)

        # Add rpm box to group
        self.box = QtWidgets.QVBoxLayout()
        self.box.addLayout(self.grid)
        self.setLayout(self.box)
    
    def update(self, rpm, redline, limiter):
        
        self.value.display(f'{rpm:6.1f}')
        
        increment = limiter / self.bar_count

        for i in range(0,self.bar_count):
            if i * increment < rpm:
                self.bars[i].setVisible(True)
                if i * increment > redline:
                    self.bars[i].setBrush(self.red_brush)
            else:
                self.bars[i].setVisible(False)