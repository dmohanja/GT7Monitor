from config import settings
from PySide6 import QtCore, QtWidgets

class SpeedGroup(QtWidgets.QGroupBox):
    def __init__(self):
        super().__init__()
        
        # Define speed factor (mps conversion to kmh/mph)
        self.use_kmh = settings.USE_KMH
        self.kmh_factor = 3.6
        self.mph_factor = 2.23694
        self.factor = self.kmh_factor if self.use_kmh else self.mph_factor

        # Define speed group box
        self.setTitle(" SPEED ")
        font = self.font()
        font.setItalic(True)
        self.setFont(font)

        # Define speed digital display
        self.value = QtWidgets.QLCDNumber()

        self.value.setDigitCount(5)
        self.value.setSmallDecimalPoint(True)
        self.value.setMinimumHeight(70)
        self.value.setSegmentStyle(QtWidgets.QLCDNumber.Outline)
        self.value.setSegmentStyle(QtWidgets.QLCDNumber.SegmentStyle.Flat)
        self.value.setStyleSheet("border-style: none;")

        # Define button to switch units
        self.units_button = QtWidgets.QPushButton("KM/H" if self.use_kmh else "MPH")
        self.units_button.setMinimumWidth(40)

        # Define grid to place everything
        self.grid = QtWidgets.QGridLayout()
        self.grid.addWidget(self.value,0,0)
        self.grid.addWidget(self.units_button,0,1)
        self.grid.setColumnStretch(0,1)
        self.grid.setColumnStretch(0,2)

        # Add grid to group
        self.setLayout(self.grid)

        # Connect units button to slot
        self.units_button.clicked.connect(self.switch_units)

    def update(self,speed):
        self.value.display(f'{(speed * self.factor):4.1f}')
    
    @QtCore.Slot()
    def switch_units(self):
        if self.use_kmh:
            self.use_kmh = False
            self.factor = self.mph_factor
            self.units_button.setText("MPH")
        else:
            self.use_kmh = True
            self.factor = self.kmh_factor
            self.units_button.setText("KM/H")