import os
import sys, json
import numpy as np
from pathlib import Path
from . import utils

def halo():
    """Menyapa dunia."""
    print("Halo dunia!")

def tambah(a, b=1):
    pesan = "ini variabel, bukan docstring"
    """string di baris kedua juga bukan docstring"""
    print(a + b)
    return a + b