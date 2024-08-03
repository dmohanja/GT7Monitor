from config import formats, settings
from PySide6 import QtCore, QtWidgets, QtGui
from gui.LiveTab import rpm, speed, gear, fuel

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        global data
        data = formats.tel_data

        # Set window title
        self.setWindowTitle("GT7 Telemetry Monitor")

        # Define start/stop button
        self.started = True if settings.START_ON_LAUNCH else False
        self.start_stop_button = QtWidgets.QPushButton("Stop Tracking" if self.started else "Start Tracking")

        # Initialize speed, rpm, gear and fuel groups
        self.speed_group = speed.SpeedGroup()
        self.rpm_group = rpm.RpmGroup()
        self.gear_group = gear.GearGroup()
        self.fuel_group = fuel.FuelGroup()

        # Add groups to grid
        self.grid = QtWidgets.QGridLayout()
        #self.speed_rpm_grid.addWidget(self.rpm_group,0,0)
        self.grid.addWidget(self.rpm_group,1,0)
        self.grid.addWidget(self.speed_group,1,1)
        self.grid.addWidget(self.gear_group,0,0)
        self.grid.addWidget(self.fuel_group,0,1)
        self.grid.setColumnStretch(0,1)
        self.grid.setColumnStretch(1,1)
        
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.start_stop_button)
        self.layout.addLayout(self.grid)

        # Connect start/stop button signal/slot
        self.start_stop_button.clicked.connect(self.start_stop)

    # Start/stop slot
    @QtCore.Slot()
    def start_stop(self):
        if not self.started:
            self.start_stop_button.setText("Stop Tracking")
            self.started = True
        else:
            self.start_stop_button.setText("Start Tracking")
            self.zero_data()
            self.started = False

    # Update all data
    def update_data(self,shared_data,lock):
        # Get lock
        locked = lock.acquire(timeout=0.05)
        try:
            if locked:
                if self.started:
                    self.rpm_group.update(shared_data['rpm'])
                    self.speed_group.update(shared_data['speed'])
                    self.gear_group.update(shared_data['gear'])
                    self.fuel_group.update(shared_data['fuel_lvl'])
                    shared_data['continue'] = True
                else:
                    shared_data['continue'] = False
        finally:
            lock.release()
    
    # Zero all data
    def zero_data(self):
        self.rpm_group.update(0)
        self.speed_group.update(0.0)
        self.gear_group.update(0)
        self.fuel_group.update(0.0)