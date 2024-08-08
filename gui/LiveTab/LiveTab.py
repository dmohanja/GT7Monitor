from config import formats, settings
from PySide6 import QtCore, QtWidgets
from gui.LiveTab import FuelGroup, GearGroup, RpmGroup, SpeedGroup
from gui import SimState

class LiveTab(QtWidgets.QVBoxLayout):
    def __init__(self):
        super().__init__()
        
        # Initialize speed, rpm, gear and fuel groups
        self.speed_group = SpeedGroup.SpeedGroup()
        self.rpm_group = RpmGroup.RpmGroup()
        self.gear_group = GearGroup.GearGroup()
        self.fuel_group = FuelGroup.FuelGroup()

        # Create left grid
        self.l_grid = QtWidgets.QGridLayout()
        self.l_grid.addWidget(self.gear_group,0,0)
        self.l_grid.addWidget(self.rpm_group,1,0)
        self.l_grid.setRowStretch(0,3)
        self.l_grid.setRowStretch(1,2)

        # Create right grid
        self.r_grid = QtWidgets.QGridLayout()
        self.r_grid.addWidget(self.speed_group,0,0)
        self.r_grid.addWidget(self.fuel_group,1,0)
        self.r_grid.setRowStretch(0,1)
        self.r_grid.setRowStretch(1,3)

        # Add l/r grids to main (self) grid
        self.main_grid = QtWidgets.QGridLayout()
        self.main_grid.addLayout(self.l_grid,0,0)
        self.main_grid.addLayout(self.r_grid,0,1)
        self.main_grid.setColumnStretch(0,1)
        self.main_grid.setColumnStretch(1,1)

        # Add main grid to vbox
        self.addLayout(self.main_grid)
