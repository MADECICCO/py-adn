import os
import subprocess
import numpy as np
import tempfile
import logging
import sys
from astropy.io import fits

import time

logger = logging.getLogger(__name__)
#logging.basicConfig(level=logging.DEBUG)
import astrometry
from astrometry.util.fits import streaming_text_table

SOLVE_FIELD = 'solve-field'
WCSINFO = 'wcsinfo'


def solve_xy(xcoords, ycoords, work_dir=None):
    if work_dir is None:
        work_dir = tempfile.mkdtemp(suffix='pyadn_work')
    logger.debug("working in %s" % work_dir)
    logger.info("writing xy text file")
    text_xy = os.path.join(work_dir, 'xy.txt')
    with open(text_xy, 'w') as fh:
        for (x, y) in zip(xcoords, ycoords):
            fh.write('%f,%f\n' % (x, y))
    logger.info("creating fits file")
    stt = streaming_text_table(text_xy, split=",",
                               skiplines=0, headerline="x,y",
                               coltypes=[np.float64, np.float64], floatvalmap={'': np.nan},
                               intvalmap=dict(null=-1))
    fits_xy = os.path.join(work_dir, 'xy.fits')
    stt.write_to(fits_xy)

    command = [SOLVE_FIELD,
               fits_xy,
               '-l', '10',  # give up after this many seconds
               '-w', '3232',
               '-e', '4864',
               '--no-plot']
    tic = time.time()
    try:
        solve_result = subprocess.check_output(command,stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        solve_result = e.output
    elapsed = time.time()-tic
    logger.info("solved in %.3f" % elapsed)
    logger.debug("Solve command: %s" % (' '.join(command)))
    logger.debug("Solve result:\n" + solve_result)
    with open(os.path.join(work_dir,'solve.log'),'w') as fh:
        fh.write(solve_result)
    return get_wcs_info(os.path.join(work_dir,'xy.wcs'))

def get_wcs_info(wcs_file):
    wcs_info_string = subprocess.check_output([WCSINFO, wcs_file])
    result = {}
    for line in wcs_info_string.splitlines():
        k,v = line.split()
        try:
            v = float(v)
        except ValueError:
            pass
        result[k] = v
    return result



if __name__ == "__main__":
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
