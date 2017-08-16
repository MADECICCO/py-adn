import os

def test_call_astrometry():
    os.system("solve-field")
    os.system("wcsinfo")