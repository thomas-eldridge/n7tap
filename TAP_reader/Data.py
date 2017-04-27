import datetime as dt
import TAP_reader_functions as tap
import numpy as np
import matplotlib.pyplot as plt # for testing and investigating

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
        retval += dt.timedelta(milliseconds=int(msec)) # confirmed as milliseconds by THIR_spec_user_guide
        return retval
    def make_lookup_table(self, words):
        new_words = np.zeros(2*len(words), float)
        for i in range(len(words)):
            new_words[2*i] = tap.do_bitcomp(words[i], 16, 31)/64.
            new_words[(2*i)+1] = tap.do_bitcomp(words[i], 0, 15)/64.
        return new_words
    def make_scan_blocks(self, words):
        """Inputs:
            - words; a numpy array of 2310 words
        Loops to prepare 10 scan blocks from the 2310 words."""
        scan_blocks = np.zeros((10, 92, 8), dtype=float)
        for i in range(10):
            scan_blocks[i] = radiance_blocks = self.prepare_scan_block(words[10*i: 10*i + 231]) # this needs to change but is for investigative purposes
        pass
    def prepare_scan_block(self, words):
        """Inputs:
            - words; a numpy array of 231 words
        I don't know what this will do."""
        nadir_scan_time = tap.do_bitcomp(words[0], 16, 31)
        scan_flags = tap.do_bitcomp(words[0], 0, 15)
        radiance_blocks = np.zeros((92,8))
        for i in range(92):
            radiance_blocks[i] = self.get_radiance_block(words[2*i:(2*(i+1))+1], i)
        return radiance_blocks
    def get_radiance_block(self, words, i):
        """Write this later"""
        if i % 2 == 0:
            bit_arr = self.a_type_arr(words)
        else:
            bit_arr = self.b_type_arr(words)
        retarr = self.set_retarr(bit_arr)
        return retarr # this should be a numpy array of length 8
    def a_type_arr(self, words):
        """Inputs:
            - words; a list of three words used to creeate the 80 bit array
        Parses the words as an a-type formulation i.e., takes all 32 bits from the
        first two words, and the first 16 bits from the third word."""
        bit_arr = np.zeros(80, dtype=bool)
        current_word = words[0]
        for i in range(32): # THIS DEFINITELY NEEDS ROBUST TESTING
            bit_arr[i] = current_word & (2**31)
            current_word = current_word << 1
        current_word = words[1]
        for i in range(32, 64):
            bit_arr[i] = current_word & (2**31)
            current_word = current_word << 1
        current_word = words[2]
        for i in range(64, 80):
            bit_arr[i] = current_word & (2**31)
            current_word = current_word << 1
        return bit_arr
    def b_type_arr(self, words):
        """Inputs:
            - words; a list of three words used to creeate the 80 bit array
        Parses the words as a b-type formulation i.e., takes the second
        16 bits from the first word, and all 32 bits from the other two words."""
        bit_arr = np.zeros(80, dtype=bool)
        current_word = words[0]
        for i in range(16):
            bit_arr[i] = current_word & (2 ** 15)
            current_word = current_word << 1
        current_word = words[1]
        for i in range(16, 48):
            bit_arr[i] = current_word & (2 ** 31)
            current_word = current_word << 1
        current_word = words[2]
        for i in range(48, 80):
            bit_arr[i] = current_word & (2 ** 31)
            current_word = current_word << 1
        return bit_arr
    def get_byte(self, bits):
        """Inputs:
            - bits; a list of 8 bits to be parsed as a byte
        Parses the bits as a byte and returns the value"""
        byte = np.int32(0) # makes sure to avoid twos complement, even when dealing with lats/lons
        for bit in bits:
            byte = byte << 1
            byte = byte | bit
        return byte
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
        self.solar_dec = swath_block[20]/1000. # in degrees
        self.vapour_table = self.make_lookup_table(swath_block[21:149]) # check number of elements
        self.window_table = self.make_lookup_table(swath_block[150:278]) # check number of elements
    def set_retarr(self, bit_arr):
        """Inputs:
            - bit_arr; an array representing the bits of an 80 bit radiance block word
        Produces an array which corresponds to the values of a radiance block."""
        retarr = np.zeros(8, float)
        retarr[0] = self.get_byte(bit_arr[0:9]) # the integer part of the latitude
        retarr[0] += self.get_byte(bit_arr[9:16])/128. # the decimal part of the latitude
        retarr[1] = self.get_byte(bit_arr[16:25]) # the integer part of the longitude
        retarr[1] += self.get_byte(bit_arr[25:32])/128. # the decimal part of the longitude
        retarr[2] = self.get_byte(bit_arr[32:40])/8. # window rad 1
        retarr[3] = self.get_byte(bit_arr[40:48])/64. # vapour rad 1
        retarr[4] = self.get_byte(bit_arr[48:56])/8. # window rad 2
        retarr[5] = self.get_byte(bit_arr[56:64])/8. # window rad 3
        retarr[6] = self.get_byte(bit_arr[64:72])/64. # vapour rad 2
        retarr[7] = self.get_byte(bit_arr[72:80])/8. # window rad 4
        return retarr
    def set_data(self, swath_block):
        """Inputs:
            - swath_block; a block of THIR data words
        Block words must correspond to data (ID=11). Words from the block are set as object attributes."""
        self.add_record(swath_block)
        self.make_scan_blocks(swath_block[1:2310])

    def set_footer(self, swath_block):
        """Inputs:
            - swath_block; a block of THIR data words
        Block words must correspond to a footer (ID=15). Words from the block are set as object attributes."""
        self.add_record(swath_block)