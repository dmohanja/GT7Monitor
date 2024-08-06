import statistics as stats
from config import formats, settings
from PySide6 import QtCore, QtWidgets, QtGui

class FuelGroup(QtWidgets.QGroupBox):
    def __init__(self):
        super().__init__()
        
        # Initialize consumption calculation parameters
        self.c1 = 0.0
        self.c2 = 0.0
        self.c3 = 0.0
        self.last_fuel = 0.0

        # Define fuel group box
        self.setTitle("FUEL")

        # Define fuel digital displays
        self.value = QtWidgets.QLCDNumber()
        self.capacity = QtWidgets.QLCDNumber()
        self.percent = QtWidgets.QLCDNumber()
        self.consumption = QtWidgets.QLCDNumber()

        self.value.setDigitCount(7)
        self.value.setSmallDecimalPoint(True)
        self.value.setMinimumHeight(30)
        self.value.setSegmentStyle(QtWidgets.QLCDNumber.Outline)
        self.value.setSegmentStyle(QtWidgets.QLCDNumber.SegmentStyle.Flat)
        self.value.setStyleSheet("border-style: none;")
        self.value_spacer = QtWidgets.QWidget()
        #self.value_spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.capacity.setDigitCount(7)
        self.capacity.setSmallDecimalPoint(True)
        self.capacity.setMinimumHeight(30)
        self.capacity.setSegmentStyle(QtWidgets.QLCDNumber.Outline)
        self.capacity.setSegmentStyle(QtWidgets.QLCDNumber.SegmentStyle.Flat)
        self.capacity.setStyleSheet("border-style: none;")
        self.capacity_spacer = QtWidgets.QWidget()
        #self.capacity_spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.percent.setDigitCount(7)
        self.percent.setSmallDecimalPoint(True)
        self.percent.setMinimumHeight(30)
        self.percent.setSegmentStyle(QtWidgets.QLCDNumber.Outline)
        self.percent.setSegmentStyle(QtWidgets.QLCDNumber.SegmentStyle.Flat)
        self.percent.setStyleSheet("border-style: none;")
        self.percent_spacer = QtWidgets.QWidget()
        #self.percent_spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.consumption.setDigitCount(7)
        self.consumption.setSmallDecimalPoint(True)
        self.consumption.setMinimumHeight(30)
        self.consumption.setSegmentStyle(QtWidgets.QLCDNumber.Outline)
        self.consumption.setSegmentStyle(QtWidgets.QLCDNumber.SegmentStyle.Flat)
        self.consumption.setStyleSheet("border-style: none;")
        self.consumption_spacer = QtWidgets.QWidget()
        #self.consumption_spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        
        # Define text for units
        self.value_txt = QtWidgets.QLabel()
        self.capacity_txt = QtWidgets.QLabel()
        self.percent_txt = QtWidgets.QLabel()
        self.consumption_txt = QtWidgets.QLabel()

        self.value_txt.setText("Remain. (l)")
        self.capacity_txt.setText("Capacity (l)")
        self.percent_txt.setText("Remain. (%)")
        self.consumption_txt.setText("Flow (l/sec)")

        # Define grid to place everything
        self.grid = QtWidgets.QGridLayout()
        #self.grid.addWidget(self.capacity_spacer,0,0)
        self.grid.addWidget(self.capacity,0,0)
        self.grid.addWidget(self.capacity_txt,0,1)
        #self.grid.addWidget(self.value_spacer,1,0)
        self.grid.addWidget(self.value,1,0)
        self.grid.addWidget(self.value_txt,1,1)
        #self.grid.addWidget(self.percent_spacer,2,0)
        self.grid.addWidget(self.percent,2,0)
        self.grid.addWidget(self.percent_txt,2,1)
        #self.grid.addWidget(self.consumption_spacer,3,0)
        self.grid.addWidget(self.consumption,3,0)
        self.grid.addWidget(self.consumption_txt,3,1)
        self.grid.setColumnStretch(0,2)
        self.grid.setColumnStretch(1,1)

        # Add fuel box to group
        #self.box = QtWidgets.QVBoxLayout()
        #self.box.addWidget(self.value)
        self.setLayout(self.grid)

    def update(self,fuel,capacity):
        
        # Current remaining fuel and total capacity
        self.value.display(f'{fuel:4.1f}')
        self.capacity.display(f'{capacity:4.1f}')
        
        # Remaining in percentage
        if capacity != 0:
            percent = fuel/capacity * 100.0
        else:
            percent = 0.0
        self.percent.display(f'{percent:4.1f}')

        # Current consumption (trailing 3 second average)
        self.c1 = self.c2
        self.c2 = self.c3
        self.c3 = self.last_fuel - fuel
        self.last_fuel = fuel
        #consumption = stats.mean([self.c1,self.c2,self.c3])

        self.consumption.display(f'{self.c3:4.1f}')