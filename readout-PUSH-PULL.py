import zmq
import time
import multiprocessing
import larpix
from larpix.format import pacman_msg_format

data = 'tcp://127.0.0.1:5556'
N_READOUTS = 1 #number of readouts
datafile = "readout-test.h5"

def readout():
    try:
        # Using SUB socket to collect data
        #reader = zmq.Context().socket(zmq.SUB)
        reader = zmq.Context().socket(zmq.PULL)
        #reader.connect(data)
        reader.bind(data)
        #reader.setsockopt(zmq.SUBSCRIBE, b"")

        messages = 0
        while True:
            print("Reading from socket:", data)
            message = reader.recv()
            print("Message received:", message)
            messages += 1
            print("Total messages received:", messages)
            #if messages >= 2019:
            #    break
            
            print("Converting to a packet...")
            packet = pacman_msg_format.parse(message)
            print("Writing to HDF5 file:", datafile)
            larpix.format.hdf5format.to_file(datafile,packet)
            print("Message written to file.")
            
            
    except:
        raise
    finally:
        reader.close()


def main():
    # Start tasks
    def start(task, *args):
        process = multiprocessing.Process(target=task, args=args)
        process.daemon = True
        process.start()
    for i in range(N_READOUTS):
        start(readout(), i)

if __name__ == "__main__":
    main()