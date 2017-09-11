#Written by Shitao Tang
# --------------------------------------------------------
import sys,logging
import os.path as osp

def add_path(path):
    if path not in sys.path:
        sys.path.insert(0, path)


this_dir = osp.dirname(__file__)
lib_path = osp.join(this_dir, 'py-R-FCN','tools')
add_path(lib_path)

lib_path = osp.join(this_dir, 'py-R-FCN','lib')
add_path(lib_path)

logging.config.fileConfig("logging.config")
