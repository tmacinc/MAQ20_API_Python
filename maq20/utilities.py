"""
This module provides a set of static functions that are meant to be used for common tasks.

Import this module by typing: from maq20 import utilities
"""
import ctypes
from math import floor, log10


def signed16_to_unsigned16(number: int) -> int:
    """
    Converts negative numbers into positive numbers.
    Raises exception if number is outside the range: [-32767, 65535]
    since those numbers cannot be represented with 16 bits signed or unsigned.
    :param number: Should be a negative number. If positive the function returns the same number
    :return: Returns the unsigned 16 bit representation of a negative number.
    """
    if number < -32767 or number > 65535:
        raise ValueError(
            "input number is outside the range of 16-bit numbers: [-32767, 65535]"
        )
    return ctypes.c_uint16(number).value


def unsigned16_to_signed16(number: int) -> int:
    """
    Convert unsigned 16 bit numbers to signed 16 bit numbers.
    Raises ValueError if input number is outside the range of 16-bit numbers: [-32767, 65535]
    :param number: input number.
    :return: signed number of type int.
    """
    if number < -32767 or number > 65535:
        raise ValueError(
            "input number is outside the range of 16-bit numbers: [-32767, 65535]"
        )
    if number <= 0:
        return number
    return ctypes.c_int16(number).value


def response_to_string(int_array) -> str:
    """
    Utility function used to convert a low level register access to ASCII characters.
    If int_array input is not valid, an empty str is returned.
    Note: any negative, or invalid type in the array is replace by a space " "
    :param int_array: input should be an array of integers returned by the low level register access functions.
    :return: a str composed of ASCII characters.
    """
    if type(int_array) is str:
        return int_array
    response_string = ""
    for c in int_array:
        try:
            response_string += chr(c)
        except (ValueError, TypeError):
            response_string += " "
    return response_string


def __generate_crc16_table():
    """ Generates a crc16 lookup table

    .. note:: This will only be generated once
    """
    result = []
    for byte in range(256):
        crc = 0x0000
        for _ in range(8):
            if (byte ^ crc) & 0x0001:
                crc = (crc >> 1) ^ 0xa001
            else:
                crc >>= 1
            byte >>= 1
        result.append(crc)
    return result


__crc16_table = __generate_crc16_table()


def compute_crc(data):
    """ Computes a crc16 on the passed in string. For modbus,
    this is only used on the binary serial protocols (in this
    case RTU).

    The difference between modbus's crc16 and a normal crc16
    is that modbus starts the crc value out at 0xffff.

    :param data: The data to create a crc16 of
    :returns: The calculated CRC
    """
    crc = 0xffff
    for a in data:
        idx = __crc16_table[(crc ^ a) & 0xff]
        crc = ((crc >> 8) & 0xff) ^ idx
    swapped = ((crc << 8) & 0xff00) | ((crc >> 8) & 0x00ff)
    return swapped


def check_crc(data, check):
    """ Checks if the data matches the passed in CRC

    :param data: The data to create a crc16 of
    :param check: The CRC to validate
    :returns: True if matched, False otherwise
    """
    return compute_crc(data) == check


def try_except(success, failure, *exceptions):
    try:
        return success()
    except exceptions or Exception:
        return failure() if callable(failure) else failure


def int16_to_int32(numbers, msb_first=True) -> int:
    """
    This function is meant to be used when a number from the register map spans two registers.
    This means that address map x is MSB, and x+1 is LSB.
    :param numbers: list of the numbers. This can be the response directly from read registers.
    :param msb_first: choose whether msb or lsb is first, True or False.
    :return: 32 bit interpretation of input.
    """
    if len(numbers) != 2:
        raise ValueError("2 numbers are needed to convert to a single value")
    return (
        (numbers[0] << 16) | numbers[1]
        if msb_first
        else (numbers[1] << 16) | numbers[0]
    )


def int32_to_uint32(i: int) -> int:
    return ctypes.c_uint32(i).value


def int32_to_int16s(number: int, msb_first=True) -> list:
    """
    Convert a number into two small enough numbers to be 16 bit.
    :param msb_first:
    :param number: a number to convert
    :return: list of integers of length 2
    """
    number_int = int(number)  # in case user passes in a string or a floating number
    return (
        [number_int >> 16, number_int & 0x0000FFFF]
        if msb_first
        else [number_int & 0x0000FFFF, number_int >> 16]
    )


def ints_to_float(numbers) -> float:
    """
    numbers[0]: integer part
    numbers[1]: decimal part
    Used for COM module PID loop controls.
    :param numbers: two integers that represent a floating point number
    :return: float type number
    """
    number_str = str(numbers[0]) + "." + str(numbers[1])
    result = float(number_str)
    return result


def float_to_ints(number) -> list:
    """
    Converts a float to a list of two integers.
    Used for COM module PID loop controls.
    :param number: float number
    :return: list of integers of size 2
    """
    if isinstance(number, int):
        return [number, 0]
    number_str = "{:.6}".format(number)
    numbers = number_str.split(".", maxsplit=1)
    return [int(x) for x in numbers]


def round_to_n(x, n: int):
    """
    Round a number to 3 significant digits
    :param x:
    :param n:
    :return:
    """
    return round(x, -int(floor(log10(x))) + (n - 1))


def counts_to_engineering_units(counts: int, p_fs, n_fs, p_fs_c, n_fs_c):
    """
    Converts a counts representation of a measurement into an engineering unit representation.
    :param counts: counts to be converted
    :param p_fs: positive full scale
    :param n_fs: negative full scale
    :param p_fs_c: positive full scale in counts
    :param n_fs_c: negative full scale in counts
    :return: float
    """

    # This is the slope, how many eng_units represents one count.
    m = (p_fs - n_fs) / (p_fs_c - n_fs_c)
    # round m to 3 significant digits.
    m_rounded = round_to_n(m, 3)
    # get how many decimal digits is the results. -2 because of the '0.'
    number_of_decimals = len(str(m_rounded)) - 2
    # calculate the offset of the counts from zero. If counts = 0 = eng units, then this is zero.
    offset = p_fs_c - (p_fs / m)
    # calculate the result and round to calculated decimals.
    return round((counts - offset) * m, number_of_decimals)


def engineering_units_to_counts(eng_value, p_fs, n_fs, p_fs_c, n_fs_c) -> int:
    """
    Converts an Eng Value to the respective Count representation based on range information.
    :param eng_value: number
    :param p_fs: positive full scale
    :param n_fs: negative full scale
    :param p_fs_c: positive full scale in counts
    :param n_fs_c: negative full scale in counts
    :return: integer
    """
    m = (p_fs - n_fs) / (p_fs_c - n_fs_c)
    offset = p_fs_c - (p_fs / m)
    return int(round((eng_value / m) + offset))


def engineering_units_to_counts_dict_input(in_val, range_information: dict) -> int:
    """
    Wrapper of engineering_units_to_counts() that takes a dictionary as an input.
    :param in_val: eng_value to be converted
    :param range_information: a dict() that contains range information, returned by MAQ20Object.get_ranges_information
    :return: integer
    """
    return engineering_units_to_counts(
        in_val,
        range_information["Engineering+FS"],
        range_information["Engineering-FS"],
        range_information["CountValue+FS"],
        range_information["CountValue-FS"],
    )


def counts_to_engineering_units_dict_input(counts: int, range_information: dict):
    """
    Wrapper of counts_to_engineering_units() that takes a dictionary as an input.
    :param counts: counts to be converted
    :param range_information: a dict() that contains range information, returned by MAQ20Object.get_ranges_information
    :return: number
    """
    return counts_to_engineering_units(
        counts,
        range_information["Engineering+FS"],
        range_information["Engineering-FS"],
        range_information["CountValue+FS"],
        range_information["CountValue-FS"],
    )
