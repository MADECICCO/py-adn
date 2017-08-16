import numpy as np
from pyadn.utils import solve_xy

def test_solve_xy():
    example = """2439,3737
            1023,2780
            173,2703
            2294,1715
            3148,4113
            994,1679
            1174,851
            3065,654
            2809,2402
            1973,494
            1522,2176
            2502,1418
            1338,3606
            2205,3153
            588,1889
            849,3730
            2655,2171
            2473,948
            2391,1143
            1527,1518
            587,1530
            909,4849
            1246,1984
            455,455"""
    lines = example.split()
    xy = np.array([(float(z.split(',')[0]),float(z.split(',')[1])) for z in lines])
    print xy.shape
    print solve_xy(xy[:,0],xy[:,1])