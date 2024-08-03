import sys, time, threading
import logging as log
from config import formats, settings
from PySide6 import QtCore, QtWidgets, QtGui

# Set log level
if settings.DEBUG:
    log.basicConfig(stream=sys.stderr, level=log.DEBUG)
else:
    log.basicConfig(stream=sys.stderr, level=log.INFO)


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

        # Define information text
        self.car_text   = QtWidgets.QLabel("TEST CAR",   alignment=(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop))
        self.track_text = QtWidgets.QLabel("TEST TRACK", alignment=(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop))

        # Define speed and RPM group boxes
        self.speed_group = QtWidgets.QGroupBox()
        self.rpm_group   = QtWidgets.QGroupBox()
        self.speed_group.setTitle("SPEED")
        self.rpm_group.setTitle("RPM")

        # Define RPM 'progress bar'
        self.rpm_bar = QtWidgets.QProgressBar()

        # Define speed and RPM digital displays
        self.rpm_value = QtWidgets.QLCDNumber()
        self.speed_value = QtWidgets.QLCDNumber()

        self.rpm_value.setDigitCount(7)
        self.rpm_value.setSmallDecimalPoint(True)
        self.rpm_value.setMinimumHeight(150)
        self.rpm_value.setSegmentStyle(QtWidgets.QLCDNumber.Outline)
        self.rpm_value.setSegmentStyle(QtWidgets.QLCDNumber.SegmentStyle.Flat)

        self.rpm_value.setDigitCount(5)
        self.rpm_value.setSmallDecimalPoint(True)
        self.speed_value.setMinimumHeight(150)
        self.speed_value.setSegmentStyle(QtWidgets.QLCDNumber.Outline)
        self.speed_value.setSegmentStyle(QtWidgets.QLCDNumber.SegmentStyle.Flat)

        # Define grids for group boxes
        self.rpm_box = QtWidgets.QVBoxLayout()
        self.rpm_box.addWidget(self.rpm_value)
        self.speed_box = QtWidgets.QVBoxLayout()
        self.speed_box.addWidget(self.speed_value)

        # Add speed and rpm boxes to group
        self.speed_group.setLayout(self.speed_box)
        self.rpm_group.setLayout(self.rpm_box)

        # Add groups to grid
        self.speed_rpm_grid = QtWidgets.QGridLayout()
        self.speed_rpm_grid.addWidget(self.rpm_group,0,0)
        self.speed_rpm_grid.addWidget(self.speed_group,0,1)
        self.speed_rpm_grid.setColumnStretch(0,6)
        self.speed_rpm_grid.setColumnStretch(1,7)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.start_stop_button)
        self.layout.addWidget(self.car_text)
        self.layout.addWidget(self.track_text)
        self.layout.addLayout(self.speed_rpm_grid)

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
                    self.rpm_value.display(f'{shared_data['rpm']:6.1f}')
                    self.speed_value.display(f'{shared_data['speed']:4.1f}')
                    shared_data['continue'] = True
                else:
                    shared_data['continue'] = False
        finally:
            lock.release()
    
    # Zero all data
    def zero_data(self):
        self.rpm_value.display(f'0.0')
        self.speed_value.display(f'0.0')


def display(shared_data,lock):

    app = QtWidgets.QApplication()

    window = MainWindow()
    window.resize(480, 320)
    window.show()
    
    # Start the receiving process
    t_loop = threading.Thread(target=loop, args=[shared_data,lock,window])
    t_loop.start()

    app.exec()
    
    t_loop.join()

def loop(shared_data,lock,widget):
    log.debug("display, outside loop: shared_data.continue: " + str(shared_data['continue']))
    log.debug("display, outside loop: shared_data.rpm: " + str(shared_data['rpm']))
    log.debug("display, outside loop: shared_data.speed: " + str(shared_data['speed']))

    while True:
        log.debug("display: shared_data.continue: " + str(shared_data['continue']))
        log.debug("display: shared_data.rpm: " + str(shared_data['rpm']))
        log.debug("display: shared_data.speed: " + str(shared_data['speed']))
        widget.update_data(shared_data,lock)
        time.sleep(0.1)
