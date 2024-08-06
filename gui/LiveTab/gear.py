from config import formats, settings
from PySide6 import QtCore, QtWidgets, QtGui

class GearGroup(QtWidgets.QGroupBox):
    def __init__(self):
        super().__init__()
        
        # Define gear group box
        self.setTitle("GEAR")

        # Define gear digital displays
        self.value = QtWidgets.QLCDNumber()
        self.suggested = QtWidgets.QLCDNumber()

        self.value.setDigitCount(2)
        self.value.setSmallDecimalPoint(False)
        self.value.setMinimumHeight(140)
        self.value.setSegmentStyle(QtWidgets.QLCDNumber.Outline)
        self.value.setSegmentStyle(QtWidgets.QLCDNumber.SegmentStyle.Flat)
        self.value.setStyleSheet("border-style: none;")

        self.suggested.setDigitCount(2)
        self.suggested.setSmallDecimalPoint(False)
        self.suggested.setMinimumHeight(70)
        self.suggested.setSegmentStyle(QtWidgets.QLCDNumber.Outline)
        self.suggested.setSegmentStyle(QtWidgets.QLCDNumber.SegmentStyle.Flat)
        self.suggested.setStyleSheet("border-style: none;")
        palette = self.suggested.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColor(255, 0, 0))
        self.suggested.setPalette(palette)

        # Define grids to place value, suggested gear and +/-
        self.minor_grid = QtWidgets.QGridLayout()
        self.minor_grid.addWidget(self.suggested,1,0)
        self.minor_grid.setRowStretch(0,1)
        self.minor_grid.setRowStretch(1,2)

        self.major_grid = QtWidgets.QGridLayout()
        self.major_grid.addWidget(self.value,0,0)
        self.major_grid.addItem(self.minor_grid,0,1)
        self.major_grid.setColumnStretch(0,2)
        self.major_grid.setColumnStretch(1,1)

        # Add gear box to group
        self.setLayout(self.major_grid)

    def update(self,gear,suggested):
        self.value.display('-' if gear == 0 else gear)
        self.suggested.display('' if gear == suggested or suggested == 15 else suggested)
        