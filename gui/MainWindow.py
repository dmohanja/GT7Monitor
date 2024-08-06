from config import formats, settings
from PySide6 import QtCore, QtWidgets, QtGui
from gui.LiveTab import rpm, speed, gear, fuel

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
        self.grid.setRowStretch(0,2)
        self.grid.setRowStretch(1,1)
        
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addLayout(self.grid)
        self.layout.addWidget(self.start_stop_button)

        # Connect start/stop button signal/slot
        self.start_stop_button.clicked.connect(self.start_stop)

        # Create QTimers for each update period
        self.timer_10fps = QtCore.QTimer()
        self.timer_10fps.setInterval(100)
        self.timer_10fps.timeout.connect(lambda: self.update_10fps(shared_data, lock))
        self.timer_5fps = QtCore.QTimer()
        self.timer_5fps.setInterval(200)
        self.timer_5fps.timeout.connect(lambda: self.update_5fps(shared_data, lock))
        self.timer_1fps = QtCore.QTimer()
        self.timer_1fps.setInterval(1000)
        self.timer_1fps.timeout.connect(lambda: self.update_1fps(shared_data, lock))

        # Zero everything
        self.zero_data()

    # Start/stop slot
    @QtCore.Slot()
    def start_stop(self):
        if not self.started:
            self.start_stop_button.setText("Stop Tracking")
            self.started = True

            # Start all update timers
            self.timer_10fps.start()
            self.timer_5fps.start()
            self.timer_1fps.start()
        else:
            self.start_stop_button.setText("Start Tracking")
            self.zero_data()
            self.started = False

            # Stop all update timers
            self.timer_10fps.stop()
            self.timer_5fps.stop()
            self.timer_1fps.stop()

    # Update data (expected to be called every ~0.1 secs)
    def update_10fps(self,shared_data,lock):
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
    def update_5fps(self,shared_data,lock):
        # Get lock
        locked = lock.acquire(timeout=0.05)
        try:
            if locked:
                if self.started:
                    self.rpm_group.update_gauge(shared_data['rpm'],shared_data['rpm_redline'],shared_data['rpm_limiter'])
                    self.gear_group.update(shared_data['gear'],shared_data['suggested_gear'])
                    
                    # Only the 5fps update function will set 'continue' to True/False
                    shared_data['continue'] = True
                else:
                    shared_data['continue'] = False
        finally:
            lock.release()

    # Update data (expected to be called every ~1 sec)
    def update_1fps(self,shared_data,lock):
        # Get lock
        locked = lock.acquire(timeout=0.05)
        try:
            if locked:
                if self.started:
                    self.fuel_group.update(shared_data['fuel_lvl'])
        finally:
            lock.release()
    
    # Zero all data
    def zero_data(self):
        self.rpm_group.update_value(0)
        self.rpm_group.update_gauge(0,0,0)
        self.speed_group.update(0.0)
        self.gear_group.update(0,0)
        self.fuel_group.update(0.0)