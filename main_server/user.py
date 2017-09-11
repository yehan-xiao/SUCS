#Written by Shitao Tang
# --------------------------------------------------------
from config import conf
from google_map_engine import google_map
from baidu_map_engine import baidu_map
from connectDB import database
from manage_cache import search_xml_in_cache, save_xml_to_cache
from common import check_keys,decode_xml,check_connection_of_image_analysis_server
import json,logging,requests,xml.etree.ElementTree,hashlib,Queue,threading,os
import web
class user:
    def __init__(self,token,map_engine):
        self.token=token
        self.image_xml=[] #list to put results of image anaylsis
        self.annotation_path=os.path.join(conf.CACHE,conf.ANNOTATION)
        self.db=database.getInstance()
        self.session=web.config._session
        self.temp=None
        if map_engine==conf.GOOGLE:
            self.map_engine=google_map.getInstance()
        elif map_engine==conf.BAIDU:
            self.map_engine=baidu_map.getInstance()

    def change_map_engine(self,data):
        temp=check_keys(data,['map_engine'])
        if temp!=None:
            return temp+' not found'
        map_engine=int(data['map_engine'])
        self.session.map_engine=map_engine
        if map_engine==conf.GOOGLE:
            self.map_engine=google_map.getInstance() #map_engine to use
        elif map_engine==conf.BAIDU:
            self.map_engine=baidu_map.getInstance()
        return json.dumps("Successfully change the map engine")

    def save_image_urls_to_database(self,image_infos):
        logging.info("begin putting image urls to database")

        for image in image_infos:
            logging.info("save "+self.token+" : "+image['url']+" to database" )
            self.db.save_image_url(self.token,self.session.search_time,image['long'],image['lat'],image['url'])
        self.session.search_time+=1

    def search_by_name(self,data):
        """search places by name and center"""
        logging.info('prepare to run search_by_name')

        results,image_infos=self.map_engine.search_by_name(data)
        self.save_image_urls_to_database(image_infos)
       
        return json.dumps(results)

    def search_bounding_box(self,data):
        """search places in a boudning box """
        logging.info("prepare to run search_bounding_box")
        image_infos=self.map_engine.search_bounding_box(data)
        self.save_image_urls_to_database(image_infos)
        return len(image_infos)

    def search_coordinate(self,data):
        """search place of the coordinate"""
        logging.info("parpare to run search_coordinate")

        results,image_urls=self.map_engine.search_coordinate(data)
        self.save_image_urls_to_database(image_urls)
        if len(image_urls)!=0:
            results=json.dumps((results),len(image_urls))
        return results

    def send_image_urls(self,address,images): #search whether the images have been analysed in the cache, send image urls that haven't been analysed to image analysis server, return the reuslt
        """send image url and its md5 to address to run image ananlysis"""
        self.image_xml=search_xml_in_cache(images)
        md5s=[]
        remove=[]
        for i in xrange(len(images)):
            if self.db.get_image_seaerched(images[i][0]):
                remove.append(i)
            else:
                md5s.append(images[i][0])
        images=[i for j,i in enumerate(images) if j not in remove]

        self.db.store_image_searched(md5s)

        for md5,url in images:
            logging.info('send '+url+' to '+address)
        if len(images)>0:
            if not check_connection_of_image_analysis_server(address):
                logging.error("Lose connection of image analysis server")
                return

            response=requests.post(address+"/detect/",data=json.dumps(images))
            logging.info('receive results from '+address)
            for msg in json.loads(response.text):
                md5,url,xml=msg[0],msg[1],msg[2]
                self.image_xml.append((md5,url,xml))
                save_xml_to_cache(md5,xml)
                

    def image_analysis(self,data):
        """take image url from database and run image analysis"""
        logging.info('run image analysis')

        temp=check_keys(data,['limit','object'])
        if temp!=None:
            return temp+" not found"
        limit=int(data['limit'])
        object_name=data['object']
        image_infos=self.db.get_image_infos(self.token,self.session.search_time-1,limit)
        logging.info('generate md5 according to image url')
        images=[]
        md5_to_place={}
        for image in image_infos:
            md5=hashlib.sha224(image['url']).hexdigest()
            images.append((md5,image['url']))
            md5_to_place[md5]=(image['long'],image['lat'])

        total_size=len(images)
        group_size=total_size/conf.NUMBER_OF_IMAGE_ANALYSIS_SERVER
        thread_pool=[]
        
        for i in range(conf.NUMBER_OF_IMAGE_ANALYSIS_SERVER): #create multiple threads to distribute images to different image analysis server
            t=threading.Thread(target=self.send_image_urls,args=(conf.ADDRESSES[i],
                images[i*group_size:min((i+1)*group_size,total_size)]))
            thread_pool.append(t)
            t.start()

        for thread in thread_pool:
            thread.join()
        logging.info('all results are returned')
        results=[]
        for md5,url,xml in self.image_xml:
            longtitude,latitude=md5_to_place[md5]
            if xml!=None:
                decoded_xml=decode_xml(object_name,xml)
                if len(decoded_xml)!=0:
                    results.append({'long':longtitude,'lat':latitude,'url':url,'bounding_box':decoded_xml})
        return json.dumps(results)
