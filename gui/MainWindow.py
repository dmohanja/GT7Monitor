from config import formats, settings
from PySide6 import QtCore, QtWidgets
from gui.LiveTab import FuelGroup, GearGroup, RpmGroup, SpeedGroup
from gui import SimState

class MainWindow(QtWidgets.QWidget):
    def __init__(self, shared_data, lock):
        super().__init__()

        global data
        data = formats.tel_data

        # Set window title
        self.setWindowTitle("GT7 Telemetry Monitor")

        # Define start/stop button
        self.started = True if settings.START_ON_LAUNCH else False
        self.start_stop_button = QtWidgets.QPushButton("Stop Tracking" if self.started else "Start Tracking")
        self.start_stop_button.setMinimumHeight(35)
        self.start_stop_button.setMaximumHeight(35)

        # Initialize sim state label
        self.sim_state = SimState.SimState()

        # Initialize speed, rpm, gear and fuel groups
        self.speed_group = SpeedGroup.SpeedGroup()
        self.rpm_group = RpmGroup.RpmGroup()
        self.gear_group = GearGroup.GearGroup()
        self.fuel_group = FuelGroup.FuelGroup()

        # Create left info grid
        self.l_info_grid = QtWidgets.QGridLayout()
        self.l_info_grid.addWidget(self.gear_group,0,0)
        self.l_info_grid.addWidget(self.rpm_group,1,0)
        self.l_info_grid.setRowStretch(0,3)
        self.l_info_grid.setRowStretch(1,2)

        # Create right info grid
        self.r_info_grid = QtWidgets.QGridLayout()
        self.r_info_grid.addWidget(self.speed_group,0,0)
        self.r_info_grid.addWidget(self.fuel_group,1,0)
        self.r_info_grid.setRowStretch(0,1)
        self.r_info_grid.setRowStretch(1,3)

        # Add l/r info grids to main info grid
        self.info_grid = QtWidgets.QGridLayout()
        self.info_grid.addLayout(self.l_info_grid,0,0)
        self.info_grid.addLayout(self.r_info_grid,0,1)
        self.info_grid.setColumnStretch(0,1)
        self.info_grid.setColumnStretch(1,1)

        # Add button(s) and sim state to grid
        self.button_grid = QtWidgets.QGridLayout()
        self.button_grid.addWidget(self.sim_state,0,0)
        self.button_grid.addWidget(self.start_stop_button,0,1)

        # Add grids to main VBox layout
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addLayout(self.info_grid)
        self.layout.addLayout(self.button_grid)

        # Connect start/stop button slot
        self.start_stop_button.clicked.connect(self.start_stop)

        # Create QTimers for each update period
        self.timer_100ms = QtCore.QTimer()
        self.timer_100ms.setInterval(100)
        self.timer_100ms.timeout.connect(lambda: self.update_100ms(shared_data, lock))
        self.timer_200ms = QtCore.QTimer()
        self.timer_200ms.setInterval(200)
        self.timer_200ms.timeout.connect(lambda: self.update_200ms(shared_data, lock))
        self.timer_1000ms = QtCore.QTimer()
        self.timer_1000ms.setInterval(1000)
        self.timer_1000ms.timeout.connect(lambda: self.update_1000ms(shared_data, lock))
        self.timer_3000ms = QtCore.QTimer()
        self.timer_3000ms.setInterval(3000)
        self.timer_3000ms.timeout.connect(lambda: self.update_3000ms(shared_data, lock))

        # Zero everything
        self.zero_data()

    # Start/stop slot
    @QtCore.Slot()
    def start_stop(self):
        if not self.started:
            self.start_stop_button.setText("Stop Tracking")
            self.started = True

            # Start all update timers
            self.timer_100ms.start()
            self.timer_200ms.start()
            self.timer_1000ms.start()
            self.timer_3000ms.start()
        else:
            self.start_stop_button.setText("Start Tracking")
            self.zero_data()
            self.started = False

            # Stop all update timers
            self.timer_100ms.stop()
            self.timer_200ms.stop()
            self.timer_1000ms.stop()
            self.timer_3000ms.start()

    # Update data (expected to be called every ~0.1 secs)
    def update_100ms(self,shared_data,lock):
        # Get lock
        locked = lock.acquire(timeout=0.05)
        try:
            if locked:
                if self.started:
                    self.rpm_group.update_value(shared_data['rpm'])
                    self.speed_group.update(shared_data['speed'])
        finally:
            lock.release()

    # Update data (expected to be called every ~0.2 secs)
    def update_200ms(self,shared_data,lock):
        # Get lock
        locked = lock.acquire(timeout=0.05)
        try:
            if locked:
                if self.started:
                    self.rpm_group.update_gauge(shared_data['rpm'],shared_data['rpm_redline'],shared_data['rpm_limiter'])
                    self.gear_group.update(shared_data['gear'],shared_data['suggested_gear'])
                    self.sim_state.update(shared_data['flags'])
                    # Only the 5fps update function will set 'continue' to True/False
                    shared_data['continue'] = True
                else:
                    shared_data['continue'] = False
        finally:
            lock.release()

    # Update data (expected to be called every ~1 sec)
    def update_1000ms(self,shared_data,lock):
        # Get lock
        locked = lock.acquire(timeout=0.05)
        try:
            if locked:
                if self.started:
                    self.fuel_group.update_value(shared_data['fuel_lvl'],shared_data['fuel_cap'])
        finally:
            lock.release()
    
        # Update data (expected to be called every ~3 secs)
    def update_3000ms(self,shared_data,lock):
        # Get lock
        locked = lock.acquire(timeout=0.05)
        try:
            if locked:
                if self.started:
                    self.fuel_group.update_consumption(shared_data['fuel_lvl'])
        finally:
            lock.release()
    
    # Zero all data
    def zero_data(self):
        self.rpm_group.update_value(0)
        self.rpm_group.update_gauge(0,0,0)
        self.speed_group.update(0.0)
        self.gear_group.update(0,0)
        self.fuel_group.update_value(0.0,0.0)
        self.fuel_group.update_consumption(0.0)