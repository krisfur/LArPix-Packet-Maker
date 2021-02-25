#general imports
import time
import sys
import multiprocessing

#larpix imports
import larpix
from larpix.format import pacman_msg_format

#zmq imports
import zmq

# Prepare ports
echo = 'tcp://127.0.0.1:5554'
cmd = 'tcp://127.0.0.1:5555'
data = 'tcp://127.0.0.1:5556'

N_PACMAN = 1 #number of PACMAN cards

# Converts HDF5 files into a list of PACMAN messegaes (bytes)
def hdf5ToPackets(datafile): 
    print("Reading from:",datafile)
    packets = larpix.format.hdf5format.from_file(datafile)['packets'] #read from HDF5 file
    print("Separating into messages based on timestamp packets...")
    msg_breaks = [i for i in range(len(packets)) if packets[i].packet_type == 4 or i == len(packets)-1] #find the timestamp packets which signify message breaks
    msg_packets = [packets[i:j] for i,j in zip(msg_breaks[:-1], msg_breaks[1:])] #separate into messages
    print("Converting to PACMAN format...")
    msgs = [pacman_msg_format.format(p, msg_type='DATA', ts_pacman=p[0].timestamp) for p in msg_packets] #convert to PACMAN format
    timestamps = [p[0].timestamp for p in msg_packets] #extract timestamps
    print("Read complete. PACMAN style messages prepared.")

    # Uncomment to debug writing to HDF5 files
    '''
    print("Writing to HDF5 file:", "pacman-test.h5")
    larpix.format.hdf5format.to_file("pacman-test.h5",packets)
    print("Message written to file.")
    print("Converting to a packet...")
    packets2 = [pacman_msg_format.parse(p) for p in msgs]
    print("Writing to HDF5 file:", "readout-test.h5")
    [larpix.format.hdf5format.to_file("readout-test.h5", p) for p in packets2]
    '''
    return msgs, timestamps

# Instance of a PACMAN card
def pacman(_echo_server,_cmd_server,_data_server,messages,timestamps):
    try:
        # Set up sockets
        ctx = zmq.Context()
        cmd_socket = ctx.socket(zmq.REP)
        #data_socket = ctx.socket(zmq.PUB)
        data_socket = ctx.socket(zmq.PUSH)
        echo_socket = ctx.socket(zmq.PUB)
        '''
        socket_opts = [
            (zmq.LINGER,100),
            (zmq.RCVTIMEO,100),
            (zmq.SNDTIMEO,100)
        ]
        for opt in socket_opts:
            cmd_socket.setsockopt(*opt)
            data_socket.setsockopt(*opt)
            echo_socket.setsockopt(*opt)
        '''
        cmd_socket.bind(_cmd_server)
        #data_socket.bind(_data_server)
        data_socket.connect(_data_server)
        echo_socket.bind(_echo_server)
        
        # Send messages in intervals based on timestamps
        msgCount = 0
        for msg,timestamp,upcoming in zip(messages,timestamps,timestamps[1:]+[None]):
            data_socket.send(msg)
            msgCount += 1
            print("Total messages sent:",msgCount)
            if upcoming != None:
                print("Next message in: %ds" %(upcoming-timestamp))
                time.sleep(upcoming-timestamp)
            
    except:
        raise
    finally: #cleanup
        data_socket.close()
        cmd_socket.close()
        echo_socket.close()
        ctx.destroy()


def main(*args):
    # Fetch messages and timestamps
    messages, timestamps = hdf5ToPackets(args[0])
    start_time = time.time()
    # Start PACMAN cards
    def start(task, *args):
        process = multiprocessing.Process(target=task, args=args)
        process.daemon = True
        process.start()
    for i in range(N_PACMAN):
        start(pacman(echo,cmd,data,messages,timestamps), i)
    print("Total elapsed time:",time.time()-start_time)


if __name__ == "__main__":
    main(str(sys.argv[1]))