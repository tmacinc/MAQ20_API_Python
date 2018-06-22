exec("import _example_init")  # Only used by the examples, you don't need to do this.
from maq20 import MAQ20

maq20 = MAQ20()
module_1 = maq20[1]

print(dir(maq20))
print(dir(module_1))

print(help(maq20))
print(help(module_1))
