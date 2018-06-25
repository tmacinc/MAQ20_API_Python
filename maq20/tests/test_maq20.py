import time
import unittest

from maq20 import MAQ20


class TestMAQ20(unittest.TestCase):
    def setUp(self):
        self.maq20 = MAQ20()

    def tearDown(self):
        self.maq20.close()

    def test_read_registers(self):
        expected = [77, 65, 81, 50, 48, 45, 67, 79, 77]  # MAQ20-COM
        read0 = self.maq20.get_com().read_registers(0, 9)  # from COM module
        read1 = self.maq20.read_registers(0, 9)  # From system
        self.assertEqual(expected, read0)
        self.assertEqual(expected, read1)

    def test_low_level_methods(self):
        # System
        answer = self.maq20.read_register(0)
        self.assertEqual(77, answer)
        answer = self.maq20.read_registers(0, 1)
        self.assertEqual([77], answer)
        self.maq20.write_register(1100, 65)
        self.assertEqual(65, self.maq20.read_register(1100))
        self.maq20.write_registers(1100, [65, 66, 67, 68])
        self.assertEqual([65, 66, 67, 68], self.maq20.read_registers(1100, 4))
        self.maq20.write_registers(1100, "abcd")
        self.assertEqual([97, 98, 99, 100], self.maq20.read_registers(1100, 4))
        self.maq20.write_registers(1100, "FILE")
        self.assertEqual([70, 73, 76, 69], self.maq20.read_registers(1100, 4))
        # COM
        com = self.maq20.get_com()
        answer = com.read_register(0)
        self.assertEqual(77, answer)
        answer = com.read_registers(0, 1)
        self.assertEqual([77], answer)
        com.write_register(1100, 65)
        self.assertEqual(65, com.read_register(1100))
        com.write_registers(1100, [65, 66, 67, 68])
        self.assertEqual([65, 66, 67, 68], com.read_registers(1100, 4))
        com.write_registers(1100, "abcd")
        self.assertEqual([97, 98, 99, 100], com.read_registers(1100, 4))
        com.write_registers(1100, "FILE")
        self.assertEqual([70, 73, 76, 69], com.read_registers(1100, 4))
        # Module
        mv = self.maq20.find("MVDN")
        answer = mv.read_register(0)
        self.assertEqual(77, answer)
        answer = mv.read_registers(0, 1)
        self.assertEqual([77], answer)
        single_reg = mv.read_register(100)
        multiple_regs = mv.read_registers(100, 8)
        mv.write_register(100, 0)
        self.assertEqual(0, mv.read_register(100))
        mv.write_register(100, 1)
        self.assertEqual(1, mv.read_register(100))
        mv.write_register(100, single_reg)

        mv.write_registers(100, [0, 0, 0, 0])
        self.assertEqual([0, 0, 0, 0], mv.read_registers(100, 4))
        mv.write_registers(100, [1, 1, 1, 1])
        self.assertEqual([1, 1, 1, 1], mv.read_registers(100, 4))
        mv.write_registers(100, multiple_regs)

    def test_com_settings(self):
        com = self.maq20.get_com()  # type: COMx

        """Save current settings so that we can leave the system as it was before this example."""
        ip_address = com.read_ip_address()
        serial_port_baud = com.read_serial_port_baud()
        serial_port_parity = com.read_serial_port_parity()
        ethernet_subnet_mask = com.read_ethernet_subnet_mask()

        # IP Address
        com.write_ip_address("192.168.128.101")
        self.assertEqual([192, 168, 128, 101], com.read_ip_address())
        com.write_ip_address([192, 168, 128, 102])
        self.assertEqual([192, 168, 128, 102], com.read_ip_address())
        com.write_ip_address(ip_address)

        # Ethernet Subnet Mask
        com.write_ethernet_subnet_mask("255.255.0.1")
        self.assertEqual([255, 255, 0, 1], com.read_ethernet_subnet_mask())
        com.write_ethernet_subnet_mask([255, 255, 0, 2])
        self.assertEqual([255, 255, 0, 2], com.read_ethernet_subnet_mask())
        com.write_ethernet_subnet_mask(ethernet_subnet_mask)

        # Serial Port Baud
        com.write_serial_port_baud(5)
        self.assertEqual(38400, com.read_serial_port_baud())
        com.write_serial_port_baud(921600)
        self.assertEqual(921600, com.read_serial_port_baud())
        com.write_serial_port_baud(serial_port_baud)

        # Serial Port Parity
        com.write_serial_port_parity(0)
        self.assertEqual("None", com.read_serial_port_parity())
        com.write_serial_port_parity("EVEN")
        self.assertEqual("Even", com.read_serial_port_parity())
        com.write_serial_port_parity(serial_port_parity)

    def test_relative_and_absolute_addressing(self):
        maq20_modules = self.maq20.get_module_list()
        for maq20_module in maq20_modules:
            self.assertEqual(
                maq20_module.read_registers(0, 50),
                self.maq20.read_registers(
                    maq20_module.get_registration_number() * 2000, 50
                ),
            )

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
