"""
Shows MAQ20 initialization and prints information about the system.
"""
exec("import _example_init")  # Only used by the examples, you don't need to do this.
from maq20 import MAQ20

system0 = MAQ20(ip_address="192.168.128.100", port=502)

print(system0)
