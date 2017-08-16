#!/usr/bin/env bash

if [ -d "$HOME/an/bin" ]
then
    echo "Found cached dir"
    exit 0
fi

which python
python --version
which python2
mkdir -p ~/bin
export PATH=~/bin:${PATH}
ls -l $(which python)
ln -s $(which python) ~/bin/python
which python
python --version
which pip2
ls -l $(which pip)
ln -s $(which pip) ~/bin/pip
which pip
pip install numpy --user
pip install fitsio --user
export WCSLIB_INC="-I/usr/include/wcslib-4.20"
export WCSLIB_LIB="-lwcs"
git clone --depth=10 --branch=master https://github.com/dstndstn/astrometry.net.git
cd astrometry.net
make
make py
make extra
make test
(cd util; ./test)
(cd blind; ./test)
(cd libkd; ./test)
make install INSTALL_DIR=~/an
export PATH=${PATH}:~/an/bin
build-astrometry-index -d 3 -o index-9918.fits -P 18 -S mag -B 0.1 -s 0 -r 1 -I 9918 -M -i demo/tycho2-mag6.fits
echo -e 'add_path .\ninparallel\nindex index-9918.fits' > 99.cfg
solve-field --config 99.cfg demo/apod4.jpg  --continue
tablist demo/apod4.match
listhead demo/apod4.wcs
export PYTHONPATH=${PYTHONPATH}:~/an/lib/python
python -c "import astrometry.libkd.spherematch"
