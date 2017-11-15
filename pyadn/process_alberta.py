import solve_images
import glob
import joblib
import os
import pandas as pd


def process_dir(dirname):
    subpath = os.path.join('/data/pmc/2017_high_level_alberta/analysis/pointing_solutions/',*list(dirname.split('/')[-3:]))
    print subpath
    files = glob.glob(os.path.join(dirname,'2*'))
    files.sort()

    pp = joblib.Parallel(n_jobs=1,verbose=5)
    rows= pp([joblib.delayed(solve_images.wrapped_solve)(fn,subpath) for fn in files])
    print "processed",len(rows)
    df = pd.DataFrame([r for r in rows if r is not None])
    print "solved",len(df)
    if os.path.exists(subpath):
        df.to_pickle(subpath+'.pkl')
    else:
        print "no solutions for:",subpath

if __name__ == "__main__":
    all_dirs = glob.glob('/data/pmc/2017_high_level_alberta/data/pmc-camera-1/data*/2*')
    all_dirs.sort()
    pp = joblib.Parallel(n_jobs=24,verbose=5)
    pp([joblib.delayed(process_dir)(dirname) for dirname in all_dirs])