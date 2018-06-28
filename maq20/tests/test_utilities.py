import unittest

from maq20 import utilities as utils


class TestUtilities(unittest.TestCase):
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
        self.assertEqual("Same", utils.response_to_string("Same"))

    def test_int16_to_int32(self):
        # Test Maximum
        self.assertEqual(2147483647, utils.int16_to_int32([0x7FFF, 0xFFFF]))
        self.assertEqual(
            2147483647, utils.int16_to_int32([0xFFFF, 0x7FFF], msb_first=False)
        )
        self.assertNotEqual(0, utils.int16_to_int32([0x7FFF, 0xFFFF]))
        self.assertNotEqual(0, utils.int16_to_int32([0x7FFF, 0xFFFF], msb_first=False))
        # Test Max input
        self.assertEqual(-1, utils.int16_to_int32([0xFFFF, 0xFFFF]))
        self.assertEqual(-1, utils.int16_to_int32([0xFFFF, 0xFFFF], msb_first=False))
        # Test Wrong inputs
        self.assertRaises(ValueError, utils.int16_to_int32, [])
        self.assertRaises(ValueError, utils.int16_to_int32, [1])
        self.assertRaises(ValueError, utils.int16_to_int32, [1, 1, 1])
        # Other random tests
        self.assertEqual(0, utils.int16_to_int32([0, 0]))
        self.assertEqual(300, utils.int16_to_int32([0, 300]))
        self.assertEqual(0x0EAD0EEF, utils.int16_to_int32([0x0EAD, 0x0EEF]))
        self.assertEqual(
            0x0EEF0EAD, utils.int16_to_int32([0x0EAD, 0x0EEF], msb_first=False)
        )
        self.assertEqual(-49152, utils.int16_to_int32([-1, 0x4000]))
        self.assertEqual(
            1073807359, utils.int16_to_int32([-1, 0x4000], msb_first=False)
        )

    def test_int32_to_uint32(self):
        for i in range(0, 4294967296, 10000):
            self.assertEqual(i, utils.int32_to_uint32(i))
        self.assertEqual(0x7FFFFFFF, utils.int32_to_uint32(0x7FFFFFFF))
        self.assertEqual(0xFFFFFFFF, utils.int32_to_uint32(0xFFFFFFFF))
        # Test for Errors
        self.assertRaises(ValueError, utils.int32_to_uint32, 4294967296)
        self.assertRaises(ValueError, utils.int32_to_uint32, -2147483649)

        self.assertEqual(2147483648, utils.int32_to_uint32(-2147483648))
        self.assertEqual(2147483649, utils.int32_to_uint32(-2147483647))

    def test_int32_to_int16s(self):
        self.assertEqual([0, 0], utils.int32_to_int16s(0))
        self.assertEqual([0, 0], utils.int32_to_int16s(0, msb_first=False))
        self.assertEqual([-1, -1], utils.int32_to_int16s(0xFFFFFFFF))
        self.assertEqual([-1, -1], utils.int32_to_int16s(0xFFFFFFFF, msb_first=False))
        self.assertEqual([-1, -1], utils.int32_to_int16s(-1))
        self.assertEqual([-1, -1], utils.int32_to_int16s(-1, msb_first=False))
        self.assertEqual([-16657, 0x1234], utils.int32_to_int16s(0xBEEF1234))
        self.assertEqual(
            [0x1234, -16657], utils.int32_to_int16s(0xBEEF1234, msb_first=False)
        )

    def test_ints_to_float(self):
        self.assertEqual(4.2, utils.ints_to_float([4, 2]))
        self.assertEqual(10.10, utils.ints_to_float([10, 10]))
        self.assertEqual(500.1, utils.ints_to_float([500, 1]))
        self.assertEqual(-4.2, utils.ints_to_float([-4, 2]))
        self.assertEqual(4, utils.ints_to_float([4, 0]))
        self.assertEqual(4.0, utils.ints_to_float([4, 0]))

    def test_float_to_ints(self):
        # Test float input
        self.assertEqual([4, 2], utils.float_to_ints(4.2))
        self.assertEqual([10, 1], utils.float_to_ints(10.1))
        self.assertEqual([500, 1], utils.float_to_ints(500.1))
        self.assertEqual([-4, 2], utils.float_to_ints(-4.2))
        self.assertEqual([4, 0], utils.float_to_ints(4.0))
        self.assertEqual([4, 0], utils.float_to_ints(4.0))
        # Test integer input
        self.assertEqual([4, 0], utils.float_to_ints(4))
        self.assertEqual([10, 0], utils.float_to_ints(10))
        self.assertEqual([500, 0], utils.float_to_ints(500))
        self.assertEqual([-4, 0], utils.float_to_ints(-4))
        self.assertEqual([4, 0], utils.float_to_ints(4))
        self.assertEqual([4, 0], utils.float_to_ints(4))
