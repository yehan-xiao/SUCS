#!/bin/sh
LIST_OF_APT_PACKAGES=
"libprotobuf-dev libleveldb-dev libsnappy-dev libopencv-dev libhdf5-serial-dev protobuf-compiler 
--no-install-recommends libboost-all-dev
libgflags-dev libgoogle-glog-dev liblmdb-dev
python-dev
python-pip
python-opencv"

LIST_OF_PIP_PACKAGES=
"cython 
easydict --trusted-host pypi.douban.com
numpy matplotlib scipy scikit-image protobuf"

sudo apt-get update && apt-get install -y $LIST_OF_APT_PACKAGES
sudo pip install -y $LIST_OF_PIP_PACKAGES

sudo easy_install web.py


#install pycaffe
cd py-R-FCN/caffe
caffepath=$PWD

#############NORMAL ERROR SOLUTION###########
####ERROR "cannot find -lhdf5_hl"
cd /usr/lib/x86_64-linux-gnu
sudo ln -s libhdf5_serial.so.10.1.0 libhdf5.so
sudo ln -s libhdf5_serial_h1.so.10.0.2 libhdf5_h1.so

####ERROR "hdf5.h:no such directory"

cd $caffepath
export CPATH="/usr/include/hdf5/serial/"
#############################################

make -j8
make pycaffe

##compile faster rcnn library
cd ../lib  
make 
python setup.py install

#python caffe path
echo "export PYTHONPATH=$caffepath/python:$PYTHONPATH" >> ~/.bashrc
source ~/.bashrcc
