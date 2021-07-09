# LArPix-Packet-Maker
 Script taking LArPix HDF5 output files, converting them into PACMAN packets, and simulating a readout stream based on timestamps in the data.
 
 Requirements:
- pyzmq (tested on version 18.1.1)
- larpix-control (tested on 3.4.0)
- LArPix HDF5 data files to use it on (tested on datalog_2020_10_19_10_13_39_CEST_.h5)

## readout.py
- Establishes a SUB socket to take data from the emulated PACMAN card
- Writes received messages to HDF5 file
- Run in separate terminal to packet-maker.py, press ENTER once packet-maker.py is waiting for a signal to start sending data

## packet-maker.py
- Takes one argument: HDF5 file with LArPix data
- Converts the HDF5 data to packets, then into PACMAN style messages 
- Optionally writes those messages to file before sending
- Sends messages at a rate defined by timestamps in the data (waits as long as the difference between timestamps of each message)

## hdf5-to-print-txt.py
- Takes one argument: HDF5 file with LArPix data
- Dumps to txt files strings representing: full LArPix packets, LArPix message packet tuples, byte messages, and timestamps extracted from the HDF5