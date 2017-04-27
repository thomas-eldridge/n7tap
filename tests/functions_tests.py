from TAP_reader.TAP_reader_functions import *
from TAP_reader.Data import Data
import nose.tools as ns
import datetime as dt

def test_change_end(): # passes on my machine
    """Numerous checks have encouraged me to believe that the change_end() function behaves as expected;
    the only test that needs to be passed is to make sure that the resultant 32-bit word is not affected by a signbit,
    i.e. that if the MSB of word_arr[0] is 1, this does not make the result negative."""
    word_arr = np.zeros(4, np.int16)
    word_arr[0] = 128
    word = change_end(word_arr)
    ns.assert_equal(2**31, word)

def test_get_bitcomp():
    """Here, get_bitcomp() is tested for each individual bit being turned on."""
    for i in range(32):
        test = 2**(31-i)
        comp = get_bitcomp(i,i)
        ns.assert_equal(comp, test)

def test_do_bitcomp():
    """Here, the comparison of do_bitcomp() with the maximum extent of an n-bit number is tested (first loop),
    and the same is tested in the second loop - this time with the lower limit setting the bit length."""
    all_on = 4294967295 # the maximum extent of an unsigned 32-bit number
    val = 0
    for n in range(32):
        comp = do_bitcomp(all_on, 0, n)
        val = 2**(n+1) - 1
        ns.assert_equal(comp, val)
    for n in range(32):
        comp = do_bitcomp(all_on, n, 31)
        val = 2**(32-n) - 1
        ns.assert_equal(comp, val)

def test_Data_add_record():
    """Checks that, given a correct output from scan_block, the record_number and record_id attributes of
    the Data object are correctly appended to."""
    The_Object = Data() # declares an empty Data object
    the_block = np.zeros(100, dtype=np.int32) # doesn't matter how long the block is, as long as the first elements are correct
    the_block[0] = change_end([0, 16, 10, 0])
    The_Object.add_record(the_block)
    ns.assert_equal(The_Object.record_id[0], 10)
    ns.assert_equal(The_Object.record_number[0], 1)

def test_Data_make_datetime():
    """The data object should be able to make a datetime object from three input parameters. Check this."""
    The_Object = Data()
    year = 1978
    day_of_year = 340
    msec = 1000
    the_dt = The_Object.make_datetime(year, day_of_year, msec)
    ns.assert_equal(the_dt, dt.datetime(1978, 12, 6, second=1))

def test_Data_make_lookup_table():
    """Need to find out exactly how the lookup table is constructed."""
    The_Object = Data()
    f = open('../input/1978/340/Nimbus7-THIRCLDT_1978m1206t015025_o00592_DR6287.TAP', 'rb')
    np.fromfile(f, dtype=np.int32, count=1)
    block = scan_block(f, n_words=2324)
    The_Object.set_header(block)

def test_a_type_arr():
    word0 = 2147483658      # 1000 0000 0000 0000 0000 0000 0000 1010
    word1 = 10              # 0000 0000 0000 0000 0000 0000 0000 1010
    word2 = 524303          # 0000 0000 0000 1000 0000 0000 0000 1111
    The_Object = Data()
    the_array = The_Object.a_type_arr([word0, word1, word2])
    right_answer = [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,
                    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,
                    0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0]
    ns.assert_equal(len(the_array), len(right_answer))
    for i in range(len(the_array)):
        ns.assert_equal(the_array[i], right_answer[i])

def test_b_type_arr():
    word0 = 2147516426      # 1000 0000 0000 0000 1000 0000 0000 1010
    word1 = 10              # 0000 0000 0000 0000 0000 0000 0000 1010
    word2 = 524289          # 0000 0000 0000 1000 0000 0000 0000 0001
    The_Object = Data()
    the_array = The_Object.b_type_arr([word0, word1, word2])
    right_answer = [1,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,
                    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,
                    0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]
    ns.assert_equal(len(the_array), len(right_answer))
    for i in range(len(the_array)):
        ns.assert_equal(the_array[i], right_answer[i])

def test_get_byte():
    bits = [0,1,0,1,0,1,0,0]
    byte = 84
    The_Object = Data()
    ans = The_Object.get_byte(bits)
    ns.assert_equal(ans, byte)