#Written by Shitao Tang and Jing Zhou
# --------------------------------------------------------
from map_engine import map
from config import conf
from common import check_keys,check_float,coordinate_from_google_to_baidu,coordinate_from_baidu_to_google
import json, requests, urllib2, httplib,logging


class baidu_map(map):
    instance=None
    def __init__(self):
        self.key_number=0
        self.key=conf.BAIDU_KEY[0]
    
    @staticmethod
    def getInstance():
        if baidu_map.instance==None:
            baidu_map.instance=baidu_map()
        return baidu_map.instance

    def get_key(): #get a baidu map api key
        self.key_number=(self.key_number+1)%len(conf.BAIDU_KEY)
        self.key=conf.BAIDU_KEY[self.key_number]
    
    def generate_image_urls(self,longitude,latitude): #generate 4 images representing 4 direction for a speicific location
        urls=[]
        for i in [0,90,180,270]:
            url="http://api.map.baidu.com/panorama/v2?ak=%s&width=1000&height=512&location=%f,%f&fov=120&pitch=40&heading=%d"%(self.key,longitude,latitude,i)
            urls.append({'long':longitude,'lat':latitude,'url':url})
        return urls

    # data contains {"name":"...","max_long":"...","min_long":"...","max_lat":"...","min_lat":"..."}
    def search_by_name(self,data): #search a place in a selected area
        temp=check_keys(data,['placename','max_long','min_long','max_lat','min_lat'])
        if temp!=None:
            return (temp+ " not found",[])
       
        logging.info('begin running search_by_name')    
        placename=data['placename']
        values=[check_float(data[i],-180,180) for i in ['max_long','min_long','max_lat','min_lat']]
        for v in values:
            if v==None:
                return ("invalid value",[])
        max_long,min_long,max_lat,min_lat=values    
             
        url = "http://api.map.baidu.com/place/v2/search?query=%s&bounds=%f,%f,%f,%f&output=json&ak=%s"%(placename,min_lat,min_long,max_lat,max_long,self.key)
        temp = urllib2.urlopen(url)
        hjson = json.loads(temp.read())
        places=[]
        urls=[]

        for i in range(len(hjson["results"])):
            name = hjson["results"][i]["name"]
            longitude = hjson["results"][i]["location"]["lng"]
            latitude = hjson["results"][i]["location"]["lat"]
            info = hjson["results"][i]["detail"]

            
            places=places+[{"name":name,"longitude":longitude,"latitude":latitude,"information":info}]
            urls=urls+self.generate_image_urls(longitude,latitude)

        return (places,urls)

    def search_bounding_box(self,data):  #get all images in a selected area
        temp=check_keys(data,['max_long','min_long','max_lat','min_lat'])
        if temp!=None:
            return ({temp+ " not found"},[])
        logging.info('begin running search_bounding_box')  
        values=[check_float(data[i],-180,180) for i in ['max_long','min_long','max_lat','min_lat']]
        for v in values:
            if v==None:
                return ("invalid value",[])
        max_long_baidu,min_long_baidu,max_lat_baidu,min_lat_baidu=values
        max_long,max_lat=coordinate_from_baidu_to_google(max_long_baidu,max_lat_baidu)  #convert bd09 coordinate to gcj02 coordinate
        min_long,min_lat=coordinate_from_baidu_to_google(min_long_baidu,min_lat_baidu)    
        
        url="http://www.openstreetmap.org/api/0.6/map?bbox={},{},{},{}".format(min_long,min_lat,max_long,max_lat)
        
        urls=[]
        places=[]        
        try:
            temp = urllib2.urlopen(url)
            dom=temp.read()
            i=0
            import re
            pattern1=re.compile('lat="[0-9]+.[0-9]+" lon="[0-9]+.[0-9]+"')  #using regular expression to decode xml file
            pattern2=re.compile('[0-9]+.[0-9]+')
            
            for string in pattern1.findall(dom):
                latitude,longitude=[float(i) for i in pattern2.findall(string)] 
                longitude,latitude=coordinate_from_google_to_baidu(longitude,latitude)
                if longitude>=min_long_baidu and longitude<=max_long_baidu and latitude>=min_lat_baidu and latitude <=max_lat_baidu:
                    urls=urls+self.generate_image_urls(longitude,latitude)            
        except urllib2.HTTPError,e:
            logging.info('This bounding box cannot be found on openstreetmap.org, please try other bounding box.')
        
        return urls


    # data contains {"longtitude":"...","latitude":"..."}
    # this funciton is not very accurate due to baidu api
    def search_coordinate(self,data):  #get infomation of a location
        temp=check_keys(data,['longitude', 'latitude'])
        if temp!=None:
            return ({temp+ " not found"},[])
        values=[check_float(data[i],-180,180) for i in ['longitude','latitude']]
        for v in values:
            if v==None:
                return ("invalid value",[])
        longitude,latitude=values

        logging.info('begin running search_coordinate')
        
        url = "http://api.map.baidu.com/geocoder/v2/?&location=%f,%f&output=json&pois=1&ak=%s"%(longitude,latitude,self.key)
        temp = urllib2.urlopen(url)
        hjson = json.loads(temp.read())
        address = hjson["result"]["formatted_address"]
        info = hjson["result"]["sematic_description"]


        return ({address:{"longitude":longitude,"latitude":latitude,"information":info}},
                self.generate_image_urls(longitude,latitude))






