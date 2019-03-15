"""
"""
import os

def test_file(path):
    return os.path.isfile(os.path.expanduser(path))