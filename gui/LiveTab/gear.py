from config import formats, settings
from PySide6 import QtCore, QtWidgets, QtGui

class GearGroup(QtWidgets.QGroupBox):
    def __init__(self):
        super().__init__()
        
        # Define gear group box
        self.setTitle("GEAR")

        # Define gear digital display
        self.value = QtWidgets.QLCDNumber()

        self.value.setDigitCount(2)
        self.value.setSmallDecimalPoint(False)
        self.value.setMinimumHeight(150)
        self.value.setSegmentStyle(QtWidgets.QLCDNumber.Outline)
        self.value.setSegmentStyle(QtWidgets.QLCDNumber.SegmentStyle.Flat)

        # Add gear box to group
        self.box = QtWidgets.QVBoxLayout()
        self.box.addWidget(self.value)
        self.setLayout(self.box)

    def update(self,gear):
        self.value.display(gear)