import pandas as pd
import os
import glob
import joblib
import re
import numpy as np
from pmc_turbo.camera.image_processing.blosc_file import load_blosc_image
from pmc_turbo.camera.star_finding import blobs
from pmc_turbo.camera.image_processing.hot_pixels import HotPixelMasker
from pmc_turbo.utils.configuration import camera_data_dir
import utils as pyadn

by_camera={}
for camera in range(1,8):
    by_camera[camera] = HotPixelMasker(np.load(('/data/pmc/pre-flight/2017-05-24-rooftop-testing/hot_pixels_%d.npy' % camera)),(3232,4864))

def solve_img(filename,solutions_path='./solutions'):
    camera = int(re.findall('camera-\d',filename)[0][-1])
    img,meta = load_blosc_image(filename)
    work_dir = os.path.abspath(os.path.join(solutions_path,os.path.split(filename)[1]))
    print work_dir
    try:
        os.makedirs(work_dir)
    except OSError:
        pass
    timestamp = int(filename[-19:])
    #bf = blobs.BlobFinder(by_camera[camera].process(img),blob_threshold=7,fit_blobs=False)
    bf = blobs.BlobFinder(img,blob_threshold=12,fit_blobs=False,kernel_size=32,kernel_sigma=5)
    xcoords = np.array([blob.x for blob in bf.blobs[:20]])
    ycoords = np.array([blob.y for blob in bf.blobs[:20]])
    res = pyadn.solve_xy(xcoords,ycoords,work_dir=work_dir)
    res['timestamp'] = timestamp
    return res

def wrapped_solve(filename,solutions_path='./solutions'):
    try:
        return solve_img(filename,solutions_path=solutions_path)
    except Exception as e:
        print e
        return None

if __name__ == "__main__":
    import sys
    assert len(sys.argv) == 3
    files = glob.glob(sys.argv[1])
    files.sort()
    print "first file:",files[0]
    print "last file:", files[-11]
    pp = joblib.Parallel(n_jobs=22,verbose=5)
    rows= pp([joblib.delayed(wrapped_solve)(fn) for fn in files])
    print "processed",len(rows)
    df = pd.DataFrame([r for r in rows if r is not None])
    print "solved",len(df)
    df.to_pickle(sys.argv[2])
