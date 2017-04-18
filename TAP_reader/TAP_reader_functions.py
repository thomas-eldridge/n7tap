import numpy as np

# TODO: inspect anomalously negative numbers in scan_block()
# TODO: write word parser

def change_end(word_arr):
    """Inputs:
        - word_arr; an array containing the four bytes
          composing the word
    Swaps the byte order so that the endianness of the word is reversed."""
    word = np.zeros(1, dtype=np.int64) # forces type to handle 31st bit being on
    for i in range(len(word_arr)):
        word[0] = word[0] << 8
        word[0] = word[0] | word_arr[i]
    return word[0]

def get_bitcomp(lower_limit, upper_limit, word_length=32):
    """Input:
        - upper_limit; the index of the most significant bit to be turned on
        - lower_limit; the index of the least significant bit to be turned on
        - word_length (default: 32); the number of bits in a standard word
    Assumes all bits in range are on. Returns a number which can be used
    to pick out bits from within a 32-bit word."""
    bit_arr = np.zeros(word_length, dtype=np.int64)
    bit_arr[lower_limit:upper_limit+1] = 1 # add 1 to upper_limit - includes endpoint
    bitcomp = 0
    for i in range(len(bit_arr)):
        bitcomp = bitcomp << 1
        bitcomp = bitcomp | bit_arr[i]
    return bitcomp

def do_bitcomp(word, lower_limit, upper_limit):
    """Input:
        - word; the 32-bit word from which bits are to be extracted
        - upper_limit; the index of the most significant bit to consider
        - lower_limit; the index of the least significant bit to consider
    Picks out bits from within a 32-bit word. Returns the decimal value
    of the specific bits as if the bit represented by lower_limit were the
    least significant bit possible."""
    ll = 32 - (upper_limit+1)
    ul = 32 - (lower_limit+1)
    bitcomp = get_bitcomp(ll, ul)
    retval = word & bitcomp
    retval = retval >> (32-(ul+1)) # add 1 to upper_limit - avoids shifting important bit out
    return retval

def scan_block(file_pointer, n_words=2322):
    """Inputs:
        - file_pointer; a variable which points to the memory location of
          a .TAP file opened to be read as binary
        - n_words (default: 2322); the number of words to be interpreted as
          a single scan block
    Reads the next (9288 byte) block of data.
    Returns a list of (2322) 32-bit words, with endianness swapped."""
    words = np.zeros(n_words, dtype=int)
    for i in range(len(words)):
        morphemes = get_morphemes(file_pointer)
        word = change_end(morphemes)
        words[i]=word
    return words

def force_signoff(array):
    """Inputs:
        - array; a numpy array, generated by np.fromfile
    Forces the 8-bit numbers read from file into 16-bit placeholders, hence ignoring signbits."""
    new_array = np.zeros(len(array), np.int16)
    for i in range(len(array)):
        new_array[i] = array[i]
    return new_array

def get_morphemes(pointer):
    bytes = force_signoff(np.fromfile(pointer, dtype=np.int8, count=4))  # each 32-bit word is made of four 8-bit morphemes
    morphemes = np.zeros(bytes.shape, dtype=np.int16)
    for i in range(len(bytes)):
        if bytes[i] != abs(bytes[i]):
            morpheme = twos_complement(abs(bytes[i]),8)
            morphemes[i] = morpheme
        else:
            morphemes[i] = bytes[i]
    return morphemes

def check_ID(block, error_catching=True):
    """Inputs:
        - block; a block of words, usually 2322 words long
        - error_catching; a boolean representing whether or not
          to raise an error when physical record numbers do not match record IDs
          (default = True)
    Uses external functions to find the ID of this block as either
    a header, data record, or a footer. Returns the ID."""
    foreign_word = block[0]
    physical_record_number = do_bitcomp(foreign_word, 20, 31)
    record_ID = do_bitcomp(foreign_word, 8, 15)
    if error_catching:
        ID_errors(physical_record_number, record_ID) # raises an error if necessary
    return record_ID

def ID_errors(number, record_type):
    """Inputs:
        - number; the index of the record in the file
        - record_type; the identifier of the record (10, 11 or 15).
    If the physical record number does not match those permitted
    for the record type, raises an error."""
    error = False
    if record_type == 10:
        if number != 1:
            error = True
        else:
            pass
    elif (record_type == 11) or (record_type == 15):
        if (number <= 1) or (number >502):
            error = True
        else:
            pass
    else:
        pass
    if error:
        raise ValueError('Record ID %i does not match record number %i' % (record_type, number))
    else:
        print 'record number = %i' % number
    return

def flip_bits(value, N):
    """Inputs:
        - value; an integer with bit length less than N
        - N; the number of bits about which bits should be flipped
    For an N-bit number, turns the on bits off and the off bits on."""
    bits = np.zeros((N), bool)
    for i in range(len(bits)):
        bits[i] = value & 1
        value = value >> 1
    new_value = 0
    for bit in ~bits[::-1]:
        new_value = new_value << 1
        new_value = new_value | bit
    return new_value

def twos_complement(value, bitlength):
    """Inputs:
        - value; the raw value of the number to find the compliment of
        - bitlength; the number of bits about which 2's compliment is to be taken
    Returns the 2's compliment of value."""
    new_val = flip_bits(value, bitlength)
    new_val += 1
    return new_val

def treat_block(File, block, error_catching=True):
    """Inputs:
        - File; an object for storage of Nimbus 7 data and attributes,
                to be appended to via class methods
        - block; an array of words representing the TAP block. One of:
              - header (ID=10),
              - data (ID=11),
              - footer (ID=15).
    Switches to the specific block treatment functions dependent on the block ID."""
    end = False
    if check_ID(block, error_catching) == 10:
        treat_as_header(block, File)
    elif check_ID(block, error_catching) == 11:
        treat_as_data(block, File)
    elif check_ID(block, error_catching) == 143: # may change to 15 later
        treat_as_footer(block, File)
        end = True
    return end

def treat_as_header(block, File):
    """Inputs:
        - block; an array of words representing a TAP block. ID should be 10 (header)
        - File; an object for storage of Nimbus 7 data and attributes,
                to be appended to via class methods
        Appends to the File object according to \'header\' rules."""

def treat_as_data(block, File):
    """Inputs:
        - block; an array of words representing a TAP block. ID should be 11 (data)
        - File; an object for storage of Nimbus 7 data and attributes,
                to be appended to via class methods
        Appends to the File object according to \'data\' rules."""

def treat_as_footer(block, File):
    """Inputs:
        - block; an array of words representing a TAP block. ID should be 143 (footer)
        - File; an object for storage of Nimbus 7 data and attributes,
                to be appended to via class methods
        Appends to the File object according to '/footer'/ rules."""

def write_nc(File):
    """Inputs:
        - File; an object for storage of Nimbus 7 data and attributes
    Writes the File object to a NetCDF."""