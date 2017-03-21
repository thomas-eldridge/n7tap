import numpy as np

# TODO: write word parser

def change_end(word_arr):
    """Inputs:
        - word_arr; an array containing the four bytes
          composing the word
    Swaps the byte order so that the endianness of the word is reversed."""
    word = 0
    for i in range(len(word_arr)):
        word = word << 8
        word = word | word_arr[i]
    return word

def get_bitcomp(lower_limit, upper_limit):
    """Input:
        - upper_limit; the index of the most significant bit to be turned on
        - lower_limit; the index of the least significant bit to be turned on
    Assumes all bits in range are on. Returns a number which can be used
    to pick out bits from within a 32-bit word."""
    bit_arr = np.zeros(32, dtype=int)
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
    bitcomp = get_bitcomp(lower_limit, upper_limit)
    retval = word & bitcomp
    retval = retval >> (32-(upper_limit+1)) # add 1 to upper_limit - avoids shifting important bit out
    return retval

