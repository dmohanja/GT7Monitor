import multiprocessing as mp
import logging as log
import sys
import rx
from gui.MainWindow import MainWindow
from PySide6 import QtWidgets
from config import formats, settings

if __name__ == '__main__':

    # Set log level
    if settings.DEBUG:
        log.basicConfig(stream=sys.stderr, level=log.DEBUG)
    else:
        log.basicConfig(stream=sys.stderr, level=log.INFO)

    # Create lock and shared dictionary
    lock = mp.Lock()
    shared_data = mp.Manager().dict()

    # Add telemetry data to shared dict
    shared_data.update(formats.tel_data)
    # Add Continue flag to shared dict
    shared_data['continue'] = True if settings.START_ON_LAUNCH else False
    # Add Stop flag to shared dict
    shared_data['stop'] = False
    
    # Start the receiving process
    p_rx = mp.Process(target=rx.listen, args=(shared_data,lock))
    p_rx.start()

    # Start the GUI
    app = QtWidgets.QApplication()
    window = MainWindow(shared_data, lock)
    window.resize(settings.GUI_DEFAULT_RES[0], settings.GUI_DEFAULT_RES[1])
    window.show()
    app.exec()

    # GUI has quit. Set shared_data['stop'] to True to tell other processes to stop
    shared_data['stop'] = True

    # Wait for comms process to finish
    p_rx.join()

    log.debug(shared_data)

