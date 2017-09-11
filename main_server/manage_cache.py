#Written by Shitao Tang
# --------------------------------------------------------
import logging,os
from config import conf

def search_xml_in_cache(images): #return xml infomation of a list of images if they can be found in cache

    image_xml=[]
    for md5,url in images:
        xml_path=os.path.join(conf.CACHE,conf.ANNOTATION,md5+'.xml')
        if os.path.isfile(xml_path):
            logging.info('found '+md5+' in cache')
            with open(xml_path,'r') as f:
                image_xml.append((md5,url,f.read()))
                
        else:
            logging.info(md5+' not found in cache')

    return image_xml

def save_xml_to_cache(md5,xml): #save xml file
    logging.info('save '+md5+' to cache')
    path=os.path.join(conf.CACHE,conf.ANNOTATION,md5+'.xml')
    if xml!=None:
        with open(path,'w') as f:
            f.write(xml)
