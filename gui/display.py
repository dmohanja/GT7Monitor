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

    window = MainWindow()
    window.resize(480, 320)
    window.show()
    
    # Start the receiving process
    t_loop = threading.Thread(target=loop, args=[shared_data,lock,window])
    t_loop.start()

    app.exec()

    # GUI has quit. Set shared_data['stop'] to True to tell everything else to exit
    shared_data['stop'] = True
    
    # Wait for loop to exit
    t_loop.join()

def loop(shared_data,lock,widget):
    log.debug("display, outside loop: shared_data.continue: " + str(shared_data['continue']))
    log.debug("display, outside loop: shared_data.rpm: " + str(shared_data['rpm']))
    log.debug("display, outside loop: shared_data.speed: " + str(shared_data['speed']))

    while not shared_data['stop']:
        log.debug("display: shared_data.continue: " + str(shared_data['continue']))
        log.debug("display: shared_data.rpm: " + str(shared_data['rpm']))
        log.debug("display: shared_data.speed: " + str(shared_data['speed']))
        widget.update_data(shared_data,lock)
        time.sleep(0.1)
