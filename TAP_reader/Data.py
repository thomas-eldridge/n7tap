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