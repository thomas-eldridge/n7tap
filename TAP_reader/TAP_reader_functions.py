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

