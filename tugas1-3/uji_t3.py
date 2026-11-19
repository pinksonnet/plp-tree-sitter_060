import os
import sys
from pathlib import Path


def tambah(a, b):
    return a + b


def sapa(nama):
    print("Halo", nama)


def tanpa_parameter():
    return 42


class Hitung:
    def kali(self, x, y):
        return x * y


print(tambah(1, 2))
sapa("Ani")
print(Hitung().kali(2, 3))