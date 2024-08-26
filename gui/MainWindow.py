from config import settings, udp
import logging as log
import sys
from PySide6 import QtCore, QtWidgets
from gui.LiveTab import LiveTab
from gui import SimState, IpAddress

# Set log level
if settings.DEBUG:
    log.basicConfig(stream=sys.stderr, level=log.DEBUG)
else:
    log.basicConfig(stream=sys.stderr, level=log.INFO)

class MainWindow(QtWidgets.QWidget):
    def __init__(self, shared_data, lock):
        super().__init__()

        # Set window title
        self.setWindowTitle("GT7 Monitor")

        # Define start/stop button
        self.started = True if settings.START_ON_LAUNCH else False
        self.start_stop_button = QtWidgets.QPushButton("STOP" if self.started else "START")
        self.start_stop_button.setMinimumHeight(35)
        self.start_stop_button.setMaximumHeight(35)
        font = self.start_stop_button.font()
        font.setBold(True)
        self.start_stop_button.setFont(font)

        # Initialize sim state label
        self.sim_state = SimState.SimState()

        # Initialize text input
        self.ip_address = IpAddress.IpAddress()
        self.ip_address.setValue(udp.LOCALHOST_IP if settings.TEST else udp.PS5_IP)

        # Initialize tabs (and their widgets)
        self.live_tab = LiveTab.LiveTab()
        self.live_widget = QtWidgets.QWidget()
        self.live_widget.setLayout(self.live_tab)

        self.empty = QtWidgets.QWidget()

        # Add tab widgets to tab layout
        self.tabs = QtWidgets.QTabWidget()
        self.tabs.addTab(self.live_widget, 'LIVE')
        self.tabs.addTab(self.empty, 'EMPTY')

        # Add button(s) and sim state to grid
        self.button_grid = QtWidgets.QGridLayout()
        self.button_grid.addWidget(self.sim_state,0,0)
        self.button_grid.addWidget(self.ip_address,0,1)
        self.button_grid.addWidget(self.start_stop_button,0,2)

        # Add grids to main VBox layout
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.tabs)
        self.layout.addLayout(self.button_grid)

        # Connect start/stop button slot
        self.start_stop_button.clicked.connect(lambda: self.start_stop(shared_data, lock))

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
    def start_stop(self, shared_data, lock):
        if not self.started:
            # Change button text
            self.start_stop_button.setText("STOP")

            # Get lock
            locked = lock.acquire()
            try:
                if locked:
                    # Get and set IP address
                    shared_data['ip'] = self.ip_address.getIP()
                    log.info("updated IP to: " + shared_data['ip'])
            finally:
                lock.release()
            

            # Indicate to other processes
            shared_data['continue'] = True
            self.started = True

            # Start all update timers
            self.timer_100ms.start()
            self.timer_200ms.start()
            self.timer_1000ms.start()
            self.timer_3000ms.start()
        else:
            # Change button text
            self.start_stop_button.setText("START")

            # Clear data
            self.zero_data()

            # Indicate to other processes
            shared_data['continue'] = False
            self.started = False

            # Stop all update timers
            self.timer_100ms.stop()
            self.timer_200ms.stop()
            self.timer_1000ms.stop()
            self.timer_3000ms.stop()

    # Update data (expected to be called every ~0.1 secs)
    def update_100ms(self,shared_data,lock):
        # Get lock
        locked = lock.acquire(timeout=0.05)
        try:
            if locked:
                if self.started:
                    self.live_tab.rpm_group.update_value(shared_data['rpm'])
                    self.live_tab.speed_group.update(shared_data['speed'])
        finally:
            lock.release()

    # Update data (expected to be called every ~0.2 secs)
    def update_200ms(self,shared_data,lock):
        # Get lock
        locked = lock.acquire(timeout=0.05)
        try:
            if locked:
                if self.started:
                    self.live_tab.rpm_group.update_gauge(shared_data['rpm'],shared_data['rpm_redline'],shared_data['rpm_limiter'])
                    self.live_tab.gear_group.update(shared_data['gear'],shared_data['suggested_gear'])
                    self.sim_state.update(shared_data['flags'],shared_data['connected'])
        finally:
            lock.release()

    # Update data (expected to be called every ~1 sec)
    def update_1000ms(self,shared_data,lock):
        # Get lock
        locked = lock.acquire(timeout=0.05)
        try:
            if locked:
                if self.started:
                    self.live_tab.fuel_group.update_value(shared_data['fuel_lvl'],shared_data['fuel_cap'])
        finally:
            lock.release()
    
        # Update data (expected to be called every ~3 secs)
    def update_3000ms(self,shared_data,lock):
        # Get lock
        locked = lock.acquire(timeout=0.05)
        try:
            if locked:
                if self.started:
                    self.live_tab.fuel_group.update_consumption(shared_data['fuel_lvl'])
        finally:
            lock.release()
    
    # Zero all data
    def zero_data(self):
        self.live_tab.rpm_group.update_value(0)
        self.live_tab.rpm_group.update_gauge(0,0,0)
        self.live_tab.speed_group.update(0.0)
        self.live_tab.gear_group.update(0,0)
        self.live_tab.fuel_group.update_value(0.0,0.0)
        self.live_tab.fuel_group.update_consumption(0.0)