from config import formats, settings
from PySide6 import QtCore, QtWidgets, QtGui

class SpeedGroup(QtWidgets.QGroupBox):
    def __init__(self):
        super().__init__()
        
        # Define speed factor (mps conversion to kmh/mph)
        self.use_kmh = settings.USE_KMH
        self.kmh_factor = 3.6
        self.mph_factor = 2.23694
        self.factor = self.kmh_factor if self.use_kmh else self.mph_factor

        # Define speed group box
        self.setTitle("SPEED")

        # Define speed digital display
        self.value = QtWidgets.QLCDNumber()

        self.value.setDigitCount(5)
        self.value.setSmallDecimalPoint(True)
        self.value.setMinimumHeight(70)
        self.value.setSegmentStyle(QtWidgets.QLCDNumber.Outline)
        self.value.setSegmentStyle(QtWidgets.QLCDNumber.SegmentStyle.Flat)
        self.value.setStyleSheet("border-style: none;")

        # Define text for units
        self.unit_txt = QtWidgets.QLabel()
        self.unit_txt.setText("KM/H" if self.use_kmh else "MPH")
        self.unit_txt.setMinimumWidth(40)

        # Define grid to place everything
        self.grid = QtWidgets.QGridLayout()
        self.grid.addWidget(self.value,0,0)
        self.grid.addWidget(self.unit_txt,0,1)
        self.grid.setColumnStretch(0,1)
        self.grid.setColumnStretch(0,2)

        # Add grid to group
        self.setLayout(self.grid)

    def update(self,speed):
        self.value.display(f'{(speed * self.factor):4.1f}')
    
    @QtCore.Slot()
    def switch_units(self):
        if self.use_kmh:
            self.use_kmh = False
            self.factor = self.mph_factor
            self.unit_txt.setText("MPH")
        else:
            self.use_kmh = True
            self.factor = self.kmh_factor
            self.unit_txt.setText("KM/H")