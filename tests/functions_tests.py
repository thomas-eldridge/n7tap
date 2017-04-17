from TAP_reader.TAP_reader_functions import *
import random as rand
import nose.tools as ns

#def test_change_end():
    # how to test this?
    # remember that I want to guarantee that it works INCLUDING for the signbit

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

def test_scan_block():
    pass

