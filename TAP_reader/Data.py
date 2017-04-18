import datetime as dt
import TAP_reader_functions as tap
import numpy as np

class Data:
    def __init__(self):
    # define all class attributes
        # shared attributes:
        self.record_number = list()
        self.record_id = list()
        # 10 (header) attributes:
        self.file_number = int(0)
        self.orbit_number = int(0)
        self.start_dt = dt.datetime(1978,01,1)
        self.stop_dt = dt.datetime(1978,01,01)
        self.south_dt = dt.datetime(1978,01,01)
        self.north_dt = dt.datetime(1978,01,01)
        self.descent_lon = float(0)
        self.ascent_lon = float(0)
        self.anode_dt = dt.datetime(1978,01,01)
        self.solar_dec = float(0)
        self.vapour_table = np.zeros((256),float)
        self.window_table = np.zeros((256),float)
        # 11 (data) attributes:

    # methods:
    #   include methods for adding to attributes via the
    #       - treat_as_header
    #       - treat_as_data
    #       - treat_as_footer
    #   functions
    def add_record(self, swath_block):
        """Inputs:
            - swath_block; a block of THIR data words
        Appends the record number and ID to the appropriate attributes of the Data object."""
        id_no, rec_no = tap.check_ID(swath_block, False)
        self.record_number.append(rec_no)
        self.record_id.append(id_no)
    def make_datetime(self, year, day, msec):
        """Inputs:
            - year; the year in which data was collected
            - day; the day of the year at which data was collected
            - msec; the number of milliseconds since the start of the day
        Makes a datetime object out of the information provided."""
        retval = dt.datetime(year, 01, 01)
        retval += dt.timedelta(days=(int(day)-1))
        retval += dt.timedelta(milliseconds=int(msec)) # TEST THAT msec IS INDEED MILLISECONDS (COULD ALSO BE MICROSECONDS)
        return retval
    def make_lookup_table(self, words):
        new_words = np.zeros(2*len(words), float)
        for i in range(len(words)):
            new_words[2*i] = tap.do_bitcomp(words[i], 16, 31)/64.
            new_words[(2*i)+1] = tap.do_bitcomp(words[i], 0, 15)/64.
        return new_words
    def set_header(self, swath_block):
        """Inputs:
            - swath_block; a block of THIR data words
        Block words must correspond to a header (ID=10). Words from the block are set as object attributes."""
        self.add_record(swath_block)
        self.file_number = swath_block[1]
        self.orbit_number = swath_block[2]
        self.start_dt = self.make_datetime(swath_block[3], swath_block[4], swath_block[5])
        self.stop_dt = self.make_datetime(swath_block[6], swath_block[7], swath_block[8])
        self.south_dt = self.make_datetime(swath_block[9], swath_block[10], swath_block[11])
        self.north_dt = self.make_datetime(swath_block[12], swath_block[13], swath_block[14])
        self.descent_lon = swath_block[15]/10.
        self.ascent_lon = swath_block[16]/10.
        self.anode_dt = self.make_datetime(swath_block[17], swath_block[18], swath_block[19])
        self.solar_dec = swath_block[20]/1000.
        self.vapour_table = self.make_lookup_table(swath_block[21:149]) # check number of elements
        self.window_table = self.make_lookup_table(swath_block[150:278]) # check number of elements
    def set_data(self, swath_block):
        """Inputs:
            - swath_block; a block of THIR data words
        Block words must correspond to data (ID=11). Words from the block are set as object attributes."""
        self.add_record(swath_block)
    def set_footer(self, swath_block):
        """Inputs:
            - swath_block; a block of THIR data words
        Block words must correspond to a footer (ID=15). Words from the block are set as object attributes."""
        self.add_record(swath_block)