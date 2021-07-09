#general imports
import sys

#larpix imports
import larpix
from larpix.format import pacman_msg_format

# Converts HDF5 files into a list of PACMAN messegaes (bytes)
def hdf5ToPackets(datafile): 
    print("Reading from:",datafile)
    packets = larpix.format.hdf5format.from_file(datafile)['packets'] #read from HDF5 file
    print("Separating into messages based on timestamp packets...")
    msg_breaks = [i for i in range(len(packets)) if packets[i].packet_type == 4 or i == len(packets)-1] #find the timestamp packets which signify message breaks
    msg_packets = [packets[i:j] for i,j in zip(msg_breaks[:-1], msg_breaks[1:])] #separate into messages
    print("Converting to PACMAN format...")
    messages = [pacman_msg_format.format(p, msg_type='DATA', ts_pacman=(p[0].timestamp)) for p in msg_packets] #convert to PACMAN format
    timestamps = [p[0].timestamp for p in msg_packets] #extract timestamps
    print("Read complete. PACMAN style messages prepared.")
    return packets, msg_packets, messages, timestamps

def main(*args):
    # Fetch messages and timestamps
    HDF5Packets, messagePackets, messages, timestamps = hdf5ToPackets(args[0])
    print("Writing text dumps to file...")
    with open("HDF5Packets.txt","w") as outf:
        for i in HDF5Packets:
            outf.write(str(i))
            outf.write("\n")
    with open("MessagePackets.txt","w") as outf:
        for i in messagePackets:
            outf.write(str(i))
            outf.write("\n")
    with open("messages.txt","w") as outf:
        for i in messages:
            outf.write(str(i))
            outf.write("\n")
    with open("timestamps.txt","w") as outf:
        for i in timestamps:
            outf.write(str(i))
            outf.write("\n")
    print("Job done.")

if __name__ == "__main__":
    try:
        main(str(sys.argv[1]))
    except IndexError:
        print("ERROR - Need to provide a data file!")