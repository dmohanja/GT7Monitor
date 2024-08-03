from config import formats, settings
from PySide6 import QtCore, QtWidgets, QtGui

class FuelGroup(QtWidgets.QGroupBox):
    def __init__(self):
        super().__init__()
        
        # Define fuel group box
        self.setTitle("FUEL")

        # Define fuel digital display
        self.value = QtWidgets.QLCDNumber()

        self.value.setDigitCount(7)
        self.value.setSmallDecimalPoint(True)
        self.value.setMinimumHeight(150)
        self.value.setSegmentStyle(QtWidgets.QLCDNumber.Outline)
        self.value.setSegmentStyle(QtWidgets.QLCDNumber.SegmentStyle.Flat)

        # Add fuel box to group
        self.box = QtWidgets.QVBoxLayout()
        self.box.addWidget(self.value)
        self.setLayout(self.box)

    def update(self,fuel):
        self.value.display(f'{fuel:4.1f}')