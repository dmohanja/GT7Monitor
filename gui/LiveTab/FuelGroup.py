from PySide6 import QtWidgets

class FuelGroup(QtWidgets.QGroupBox):
    def __init__(self):
        super().__init__()
        
        # Initialize consumption and flow calculation parameters
        self.flow_hist = [0.0, 0.0, 0.0]
        self.last_fuel = 0.0

        # Define fuel group box
        self.setTitle("FUEL")

        # Define fuel digital displays
        self.value = QtWidgets.QLCDNumber()
        self.capacity = QtWidgets.QLCDNumber()
        self.flow = QtWidgets.QLCDNumber()

        self.value.setDigitCount(7)
        self.value.setSmallDecimalPoint(True)
        self.value.setMinimumHeight(30)
        self.value.setSegmentStyle(QtWidgets.QLCDNumber.Outline)
        self.value.setSegmentStyle(QtWidgets.QLCDNumber.SegmentStyle.Flat)
        self.value.setStyleSheet("border-style: none;")
        self.value_spacer = QtWidgets.QWidget()

        self.capacity.setDigitCount(7)
        self.capacity.setSmallDecimalPoint(True)
        self.capacity.setMinimumHeight(30)
        self.capacity.setSegmentStyle(QtWidgets.QLCDNumber.Outline)
        self.capacity.setSegmentStyle(QtWidgets.QLCDNumber.SegmentStyle.Flat)
        self.capacity.setStyleSheet("border-style: none;")
        self.capacity_spacer = QtWidgets.QWidget()

        self.flow.setDigitCount(7)
        self.flow.setSmallDecimalPoint(True)
        self.flow.setMinimumHeight(30)
        self.flow.setSegmentStyle(QtWidgets.QLCDNumber.Outline)
        self.flow.setSegmentStyle(QtWidgets.QLCDNumber.SegmentStyle.Flat)
        self.flow.setStyleSheet("border-style: none;")
        self.flow_spacer = QtWidgets.QWidget()
        
        # Define text for units
        self.value_txt = QtWidgets.QLabel()
        self.capacity_txt = QtWidgets.QLabel()
        self.flow_txt = QtWidgets.QLabel()

        self.value_txt.setText("Remain. (%)")
        self.capacity_txt.setText("Capacity (%)")
        self.flow_txt.setText("Flow (%/sec)")

        # Define grid to place everything
        self.grid = QtWidgets.QGridLayout()
        self.grid.addWidget(self.capacity,0,0)
        self.grid.addWidget(self.capacity_txt,0,1)
        self.grid.addWidget(self.value,1,0)
        self.grid.addWidget(self.value_txt,1,1)
        self.grid.addWidget(self.flow,2,0)
        self.grid.addWidget(self.flow_txt,2,1)
        self.grid.setColumnStretch(0,2)
        self.grid.setColumnStretch(1,1)

        # Add grid to group
        self.setLayout(self.grid)

    def update_value(self,fuel,capacity):
        # Current remaining fuel and total capacity
        self.value.display(f'{fuel:4.1f}')
        self.capacity.display(f'{capacity:4.1f}')
    
    def update_consumption(self,fuel):
        # Current fuel flow (trailing 3 second average)
        self.flow_hist[2] = self.flow_hist[1]
        self.flow_hist[1] = self.flow_hist[0]
        self.flow_hist[0] = self.last_fuel - fuel
        self.last_fuel = fuel

        flow = (self.flow_hist[0] + self.flow_hist[1] + self.flow_hist[2]) / 3.0
        # Only display if result is positive
        if flow >= 0:
            self.flow.display(f'{flow:4.1f}')