#Written by Shitao Tang，Yehan Xiao
# --------------------------------------------------------
from easydict import EasyDict as edict
__C=edict()

conf=__C
#classes that can be detected
__C.CLASSES = ('__background__', # always index 0
'manhole')

#name of the net
__C.net_name="resnet50_rfcn_ohem_iter_800"

#use gpu or cpu to run
__C.mode='gpu'

#confidence greater than this thresh will be detected
__C.SOFTMAX_THRESH=0.4
#non maximum suppression 
__C.NMS_THRESH=0.3

#images path
__C.IMAGES_DIR="images"

#number of gpus to use
__C.NUMBER_OF_GPUS=1

#number of thread to download images
__C.NUMBER_OF_THREADS_TO_DOWNLOAD_IMAGES=10
