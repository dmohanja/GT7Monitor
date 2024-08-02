import multiprocessing as mp
import time
import rx, gui_pyside6
from config import formats, settings

if __name__ == '__main__':

    lock = mp.Lock()
    shared_data = mp.Manager().dict()

    # Add telemetry data to shared dict
    shared_data.update(formats.tel_data)

    # Add Continue flag
    shared_data['continue'] = True if settings.START_ON_LAUNCH else False

    # Add Stop flag
    shared_data['stop'] = False
    
    # Start the receiving process
    p_rx = mp.Process(target=rx.listen, args=(shared_data,lock))
    p_rx.start()

    # Start the GUI process
    p_disp = mp.Process(target=gui_pyside6.display, args=(shared_data,lock))
    p_disp.start()

    # Stop monitoring
    #time.sleep(10)
    #shared_data['continue'] = False

    # Wait for receiving process to finish
    p_rx.join()

    # Wait for GUI process to finish
    p_disp.join()

    print(shared_data)

