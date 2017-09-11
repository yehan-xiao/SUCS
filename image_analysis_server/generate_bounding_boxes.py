#Written by Shitao Tang
# --------------------------------------------------------
import __init__
from fast_rcnn.test import im_detect
from fast_rcnn.nms_wrapper import nms
from fast_rcnn.config import cfg
import numpy as np
import caffe, os, sys, cv2,logging
from write_annotation import generate_image_xml
from config import conf

CLASSES = conf.CLASSES

def detectImageByName(net,img_name,gpu_id=0):
    """Using net to detect image by its img_name with gpu_id. The result is returned as xml format"""
    logging.info("detection by image name begins")
    images_dir=conf.IMAGES_DIR
    image_path=os.path.join(images_dir,img_name)
    if not os.path.isfile(image_path):
        logging.error("can't find image_path") 

    if conf.mode=='cpu':
        caffe.set_mode_cpu()
    else:
        caffe.set_mode_gpu()
        caffe.set_device(gpu_id)
        cfg.GPU_ID = gpu_id

    logging.info("begin analyzing "+img_name)
    img=cv2.imread(image_path)
    if img==None:
        return None
    scores,boxes=im_detect(net,img)
    logging.info("finish analyzing "+img_name)

    SOFTMAX_THRESH = conf.SOFTMAX_THRESH
    NMS_THRESH = conf.NMS_THRESH

    bounding_box={}
    for cls_ind, cls in enumerate(CLASSES[1:]):
        cls_ind += 1 # because we skipped background
        cls_boxes = boxes[:, 4:8]
        cls_scores = scores[:, cls_ind]
        dets = np.hstack((cls_boxes,
                          cls_scores[:, np.newaxis])).astype(np.float32)
        logging.info("applying nms to class "+cls+" in "+img_name)
        keep = nms(dets, NMS_THRESH)
        logging.info("finish applying nms to class "+cls+" in "+img_name)
        dets = dets[keep, :]
        bounding_box[cls]=dets[dets[:,-1]>SOFTMAX_THRESH]

    return generate_image_xml(img_name,img.shape,bounding_box)

