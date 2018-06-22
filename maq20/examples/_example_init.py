"""
Makes maq20 importable from an example when the module is not installed system wide
"""
import imp
import os
import sys


try:
    imp.find_module("maq20")
    found = True
except ImportError:
    found = False
if not found:
    examples_dir_path = os.path.abspath(os.path.dirname(__file__))
    maq20_path = os.path.split(os.path.split(examples_dir_path)[0])[0]
    sys.path.extend([maq20_path, examples_dir_path])
