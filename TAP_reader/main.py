from Data import Data

def read_TAP_file(filename):
    """Inputs:
        - filename; a string corresponding to the complete path to a
          Nimbus 7 TAP file.
    Opens the file in read binary mode. Reads the file and writes it as a NetCDF."""
    File = Data(filename)
    write_nc(File)

if __name__=='__main__':
    read_TAP_file('../input/1978/340/Nimbus7-THIRCLDT_1978m1206t015025_o00592_DR6287.TAP')