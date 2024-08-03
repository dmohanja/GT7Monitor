from config import formats, settings
from PySide6 import QtCore, QtWidgets, QtGui

class SpeedGroup(QtWidgets.QGroupBox):
    def __init__(self):
        super().__init__()
        
        # Define speed group box
        self.setTitle("KPH")

        # Define speed digital display
        self.value = QtWidgets.QLCDNumber()

        self.value.setDigitCount(5)
        self.value.setSmallDecimalPoint(True)
        self.value.setMinimumHeight(150)
        self.value.setSegmentStyle(QtWidgets.QLCDNumber.Outline)
        self.value.setSegmentStyle(QtWidgets.QLCDNumber.SegmentStyle.Flat)

        # Add speed box to group
        self.box = QtWidgets.QVBoxLayout()
        self.box.addWidget(self.value)
        self.setLayout(self.box)

    def update(self,speed):
        self.value.display(f'{speed:4.1f}')