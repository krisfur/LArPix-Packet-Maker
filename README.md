# LArPix-Packet-Maker
 Script taking LArPix HDF5 output files, converting them into PACMAN packets, and simulating a readout stream based on timestamps in the data.
 
 Requirements:
- pyzmq (tested on version 18.1.1)
- larpix-control (tested on 3.4.0)
- LArPix HDF5 data files to use it on (tested on datalog_2020_10_19_10_13_39_CEST_.h5)

## readout.py
- Establishes a SUB socket to take data from the emulated PACMAN card
- Writes received messages to HDF5 file
- Run in separate terminal before running packet-maker.py

## packet-maker.py
- Takes one argument: HDF5 file with LArPix data
- Converts the HDF5 data to packets, then into PACMAN stryle messages 
- Sends messages at a rate defined by timestamps in the data (waits as long as the difference between timestamps of each message)
