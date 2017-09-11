#Written by Shitao Tang, Yehan Xiao
# --------------------------------------------------------
import urllib
import urllib2
import Queue
import json
import threading
import load_net
import web
import logging
from config import conf


class detect:
    net=load_net.load()

    def delete_images(self):
        """Delete images finished detected"""
        import os
        for file in os.listdir(conf.IMAGES_DIR):
            image_path=os.path.join(conf.IMAGES_DIR,file)
            os.remove(image_path)

    def download_image(self,image_url,md5):
        """Download image according to image_url and save the image as its md5 value"""
        logging.info("try downloading from "+image_url)
        try: 
            urllib2.urlopen(image_url)
            logging.info(image_url+" exists")

            saved_name=md5+'.jpg'
            import os
            saved_path=os.path.join(conf.IMAGES_DIR,saved_name)
            logging.info("downloading "+image_url+" ...")
            urllib.urlretrieve (image_url, saved_path)
            logging.info("finish downloading "+image_url)
            self.waiting_for_analysis.put((saved_name,image_url))

            self.image_analysis_semaphore.release()

        except Exception:
            logging.warning("Can't download image from "+image_url)

        self.mutex.acquire()
        self.downloading_tried+=1
        if self.downloading_tried==self.images_number:
            self.image_analysis_semaphore.release()
        self.mutex.release()

        self.number_of_threads_downloading_images_semaphore.release()

    def run_image_analysis(self,gpu_id):
        """Get image names from queue and run image analysis program using gpu_id on them. Put the results in another queue"""
        from generate_bounding_boxes import detectImageByName
        logging.info("image analysis program started")
        while self.downloading_tried<self.images_number or self.waiting_for_analysis.qsize()!=0:
            self.image_analysis_semaphore.acquire()
            if self.waiting_for_analysis.qsize()!=0:
                image_name,url=self.waiting_for_analysis.get()
                logging.info("detecting "+image_name+" ...")
                self.successfully_detected.put((image_name[0:-4],url,detectImageByName(detect.net,image_name,gpu_id)))

        self.number_of_gpus_semaphore.release()
        logging.info("exit image analysis program")

    def POST(self,name):
        """Reveice a dict{image url:md5}. Downloading these images and run detection algorithm on them. Return a dict{md5:result}. Result is stored as xml format"""
        self.waiting_for_analysis=Queue.Queue() #images waiting for detection
        self.successfully_detected=Queue.Queue() #results of the images successfully detected is put here
        self.image_analysis_semaphore=threading.Semaphore(0) #semaphore used to synchronize run_image_ananlysis and download_image
        self.number_of_threads_downloading_images_semaphore=threading.Semaphore(conf.NUMBER_OF_THREADS_TO_DOWNLOAD_IMAGES)
        self.number_of_gpus_semaphore=threading.Semaphore(conf.NUMBER_OF_GPUS)
        self.downloading_tried=0 #the number of images that have been trying to download
        self.mutex=threading.Lock() #mutex to use when writing to access downloading_tried
        
        logging.info("finish initializing class detect parameters")
        images=json.loads(web.data())
        self.images_number=len(images)


        for i in range(conf.NUMBER_OF_GPUS):
            self.number_of_gpus_semaphore.acquire()
            threading.Thread(target=self.run_image_analysis,args=(i,)).start()

        for md5,image_url in images:
            self.number_of_threads_downloading_images_semaphore.acquire()
            threading.Thread(target=self.download_image,args=(image_url,md5)).start()

        for i in range(conf.NUMBER_OF_GPUS): #make sure all the threads exits
            self.number_of_gpus_semaphore.acquire()

        for i in range(conf.NUMBER_OF_THREADS_TO_DOWNLOAD_IMAGES):
            self.number_of_threads_downloading_images_semaphore.acquire()


        result=[]
        while self.successfully_detected.qsize()!=0:
            result.append(self.successfully_detected.get())

        threading.Thread(target=self.delete_images).start()
        
        return json.dumps(result)
