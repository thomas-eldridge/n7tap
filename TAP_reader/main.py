from TAP_reader_functions import *
import os
from Data import Data

def read_TAP_file(filename):
    """Inputs:
        - filename; a string corresponding to the complete path to a
          Nimbus 7 TAP file.
    Opens the file in read binary mode. Reads the file and writes it as a NetCDF."""
    f = open(filename, 'rb') # open te file in read binary mode
    np.fromfile(f, dtype=np.int32, count=1) # skips first word - all first words in all files are identical and extraneous
    end = False
    File = Data()
    while not end:
        block = scan_block(f, n_words=2324) # unit test MUST make sure that this n_words is appropriate for all cases
        end = treat_block(File, block, False)
    write_nc(File)

if __name__=='__main__':
    read_TAP_file('../input/1978/340/Nimbus7-THIRCLDT_1978m1206t015025_o00592_DR6287.TAP')