import multiprocessing as mp
import logging as log
import sys
import rx, gui_pyside6
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

    # Start the GUI process
    p_disp = mp.Process(target=gui_pyside6.display, args=(shared_data,lock))
    p_disp.start()

    # Wait for GUI process to finish
    p_disp.join()

    # Wait for comms process to finish
    p_rx.join()

    log.debug(shared_data)

