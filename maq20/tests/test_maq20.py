import time
import unittest

from maq20 import MAQ20


class TestMAQ20(unittest.TestCase):
    def setUp(self):
        self.maq20 = MAQ20()

    def test_read_registers(self):
        read0 = self.maq20.get_com().read_registers(0, 10)
        read1 = self.maq20.read_registers(0, 10)
        self.assertEqual(read0, read1)

    def test_fail_to_connect(self):
        if float(self.maq20.get_com().get_firmware_version()[1:-1]) > 1.36:
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

    def test_set_and_read_current(self):
        i_in = self.maq20.find("ISN")
        i_out = self.maq20.find("-IO")
        currents = [i for i in range(20)]
        epsilon = 0.1 * 1e-3
        for current in currents:
            i_out[0] = current
            time.sleep(0.5)  # Allow the value to settle
            read_back = i_in[0]
            self.assertTrue(
                abs(current * 1e-3) - abs(read_back) < epsilon,
                msg="In: {} Out: {}".format(current * 1e-3, read_back),
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

        self.assertIsInstance(mv.display_ranges_information(), str)
        self.assertIsInstance(vo.display_ranges_information(), str)
        self.assertIsInstance(i_in.display_ranges_information(), str)
        self.assertIsInstance(i_out.display_ranges_information(), str)
        self.assertIsInstance(diol.display_ranges_information(), bool)
        self.assertIsInstance(dioh.display_ranges_information(), bool)
        self.assertIsInstance(tc.display_ranges_information(), str)
        self.assertIsInstance(rtd.display_ranges_information(), str)
        self.assertIsInstance(brdg.display_ranges_information(), bool)
        self.assertIsInstance(rly.display_ranges_information(), bool)
        self.assertIsInstance(freq.display_ranges_information(), str)

    def test_low_level_methods(self):
        pass
