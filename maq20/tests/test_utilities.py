import unittest

from maq20 import utilities as utils


class TestMAQ20(unittest.TestCase):
    def test_signed16_to_unsigned16(self):
        # Test that positive numbers are not changed
        for i in range(65536):
            self.assertEqual(i, utils.signed16_to_unsigned16(i))
        # Test some negative numbers
        self.assertEqual(65535, utils.signed16_to_unsigned16(-1))
        self.assertEqual(65534, utils.signed16_to_unsigned16(-2))
        self.assertEqual(32769, utils.signed16_to_unsigned16(-32767))
        self.assertEqual(35536, utils.signed16_to_unsigned16(-30000))
        # Test some numbers outside the range
        self.assertRaises(ValueError, utils.signed16_to_unsigned16, 65536)
        self.assertRaises(ValueError, utils.signed16_to_unsigned16, -32768)
        self.assertRaises(ValueError, utils.signed16_to_unsigned16, 165536)
        self.assertRaises(ValueError, utils.signed16_to_unsigned16, -312768)

    def test_unsigned16_to_signed16(self):
        # Test that positive numbers are not changed
        for i in range(-32765, 32768):
            self.assertEqual(i, utils.unsigned16_to_signed16(i))
        # Test some negative numbers
        self.assertEqual(-1, utils.unsigned16_to_signed16(65535))
        self.assertEqual(-2, utils.unsigned16_to_signed16(65534))
        self.assertEqual(-32767, utils.unsigned16_to_signed16(32769))
        self.assertEqual(-30000, utils.unsigned16_to_signed16(35536))
        # Test some numbers outside the range
        self.assertRaises(ValueError, utils.unsigned16_to_signed16, 65536)
        self.assertRaises(ValueError, utils.unsigned16_to_signed16, -32768)
        self.assertRaises(ValueError, utils.unsigned16_to_signed16, 165536)
        self.assertRaises(ValueError, utils.unsigned16_to_signed16, -312768)

    def test_response_to_string(self):
        self.assertEqual(
            "MAQ20-COM4",
            utils.response_to_string([77, 65, 81, 50, 48, 45, 67, 79, 77, 52]),
        )
        self.assertEqual("   ", utils.response_to_string([-2, 3.0, None]))

    def test_int16_to_int32(self):
        # Test Maximum
        self.assertEqual(2147483647, utils.int16_to_int32([0x7FFF, 0xFFFF]))
        self.assertEqual(
            2147483647, utils.int16_to_int32([0xFFFF, 0x7FFF], msb_first=False)
        )
        self.assertNotEqual(0, utils.int16_to_int32([0x7FFF, 0xFFFF]))
        self.assertNotEqual(0, utils.int16_to_int32([0x7FFF, 0xFFFF], msb_first=False))
        # Test Max input
        # self.assertEqual(-1, utils.int16_to_int32([0xFFFF, 0xFFFF]))
        # self.assertEqual(-1, utils.int16_to_int32([0xFFFF, 0xFFFF], msb_first=False))
        # Test Wrong inputs
        self.assertRaises(ValueError, utils.int16_to_int32, [])
        self.assertRaises(ValueError, utils.int16_to_int32, [1])
        self.assertRaises(ValueError, utils.int16_to_int32, [1, 1, 1])

    def test_int32_to_uint32(self):
        pass

    def test_int32_to_int16s(self):
        pass

    def test_ints_to_float(self):
        pass

    def test_float_to_ints(self):
        pass

    def test_round_to_n(self):
        pass

    def test_counts_to_engineering_units(self):
        pass

    def test_engineering_units_to_counts(self):
        pass

    def test_engineering_units_to_counts_dict_input(self):
        pass

    def test_counts_to_engineering_units_dict_input(self):
        pass
