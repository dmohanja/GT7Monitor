import sys, time, threading
import logging as log
from config import formats, settings
from PySide6 import QtCore, QtWidgets, QtGui
from gui.MainWindow import MainWindow

# Set log level
if settings.DEBUG:
    log.basicConfig(stream=sys.stderr, level=log.DEBUG)
else:
    log.basicConfig(stream=sys.stderr, level=log.INFO)


def display(shared_data,lock):

    app = QtWidgets.QApplication()

    window = MainWindow(shared_data, lock)
    window.resize(480, 320)
    window.show()

    app.exec()

    # GUI has quit. Set shared_data['stop'] to True to tell other processes to stop
    shared_data['stop'] = True
