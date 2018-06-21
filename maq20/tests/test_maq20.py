import unittest
import time

from maq20 import MAQ20


class TestMAQ20(unittest.TestCase):
    def setUp(self):
        self.maq20 = MAQ20()

    def test_read_registers(self):
        read0 = self.maq20.get_com().read_registers(0, 10)
        read1 = self.maq20.read_registers(0, 10)
        self.assertEqual(read0, read1)

    def test_fail_to_connect(self):
        self.assertRaises(Exception, MAQ20, "192.168.128.200")

    def test_set_and_read_voltage(self):
        voltages = [-2.0, -1.5, -1, -0.1, 0, 0.1, .5, 1.2, 2]
        epsilon = 0.1
        vo = self.maq20.find("VO")
        mv = self.maq20.find("MVDN")
        for voltage in voltages:
            vo[0] = voltage
            time.sleep(0.5)  # Allow the value to settle
            read_back = mv[0]
            self.assertTrue(
                abs(voltage) - abs(read_back) < epsilon,
                msg="In: {} Out: {}".format(voltage, read_back),
            )
    
    def test_modules_ranges(self):
        mv = self.maq20.find("MVDN")
        vo = self.maq20.find("VO")
        i_in = self.maq20.find("ISN")
        i_out = self.maq20.find("-IO")
        diol = self.maq20.find("DIOL")
        dioh = self.maq20.find("DIOH")
        tc = self.maq20.find("TC")
        rtd = self.maq20.find("RTD")
        brdg = self.maq20.find("BRDG")
        rly = self.maq20.find("RLY20")
        freq = self.maq20.find("FREQ")

        self.assertEqual(True, mv.has_range_information())
        self.assertEqual(True, vo.has_range_information())
        self.assertEqual(True, i_in.has_range_information())
        self.assertEqual(True, i_out.has_range_information())
        self.assertEqual(False, diol.has_range_information())
        self.assertEqual(False, dioh.has_range_information())
        self.assertEqual(True, tc.has_range_information())
        self.assertEqual(True, rtd.has_range_information())
        self.assertEqual(False, brdg.has_range_information())
        self.assertEqual(False, rly.has_range_information())
        self.assertEqual(True, freq.has_range_information())
