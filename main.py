import multiprocessing as mp
import time
import rx
from config import formats

if __name__ == '__main__':

    lock = mp.Lock()
    shared_data = mp.Manager().dict()

    # Add telemetry data to shared dict
    shared_data.update(formats.tel_data)

    # Add Continue flag
    shared_data['continue'] = True
    
    p = mp.Process(target=rx.listen, args=(shared_data,lock))
    p.start()
    time.sleep(1)

    shared_data['continue'] = False
    p.join()

    print(shared_data)

