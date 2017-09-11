#Written by Shitao Tang
# --------------------------------------------------------
import __init__
import os,caffe,logging,sys
import numpy as np
from config import conf
from fast_rcnn.test import im_detect

def load():
    """preload caffe net"""
    net_name=conf.net_name

    manhole_net_path="manhole_net"
    model_path="final_models"
    prototxt_path="final_prototxt"

    prototxt_name=net_name+'.prototxt'
    model_name=net_name+'.caffemodel'
    prototxt=os.path.join(manhole_net_path,prototxt_path,prototxt_name)
    model=os.path.join(manhole_net_path,model_path,model_name)

    if not os.path.isfile(model):
        logging.error("model "+model_name+" not found. exit")
        sys.exit()

    if not os.path.isfile(prototxt):
        logging.error("prototxt "+prototxt+" not found. exit")
        sys.exit()

    logging.info("begin loading caffe net")
    net=caffe.Net(prototxt, model, caffe.TEST)
    logging.info("finish loading caffe")

    if net == None:
        logging.error("can't load caffe net. exit")
        sys.exit()

    if conf.mode=='cpu':
        caffe.set_mode_cpu()
    else:
        caffe.set_mode_gpu()

    im = 128 * np.ones((300, 500, 3), dtype=np.uint8)
    logging.info("begin processing a dummy image to warm up")
    im_detect(net,im)
    logging.info("finish processing a dummy image")
    return net
