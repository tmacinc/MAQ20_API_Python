import unittest

from maq20 import MAQ20


class TestMAQ20(unittest.TestCase):
    def setUp(self):
        self.maq20 = MAQ20()

    def test_read_registers(self):
        read0 = self.maq20.get_com().read_registers(0, 10)
        read1 = self.maq20.read_registers(0, 10)
        self.assertEquals(read0, read1)

    def test_fail_to_connect(self):
        self.assertRaises(Exception, MAQ20, "192.168.128.200")
