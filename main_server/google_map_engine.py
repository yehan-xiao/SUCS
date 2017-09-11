#Written by Shitao Tang and Benjamin John Pemberton Morse
# --------------------------------------------------------
from map_engine import map
import googlemaps
from common import check_keys,check_float
from googlemaps import client
import urllib2,logging
import xml.etree.cElementTree as ET

yourkey = 'AIzaSyAoaOH-XDMVKlm8KJoCXDLR8Twkz0rVkcY'
gmaps = googlemaps.Client(key=yourkey)

class google_map(map):
    instance=None

    @staticmethod
    def getInstance():
        if google_map.instance==None:
            google_map.instance=google_map()
        return google_map.instance
   
    # data contains {"name":"...","max_long":"...","min_long":"...","max_lat":"...","min_lat":"..."}
    def generate_image_urls(self,longitude,latitude):
        urls=[]
        for pitch,head in [(270,0),(300,0),(300,270),(300,90)]:
            url = 'https://maps.googleapis.com/maps/api/streetview?size=700x700&location={},{}&fov=120&pitch={}&heading={}&key=AIzaSyAoaOH-XDMVKlm8KJoCXDLR8Twkz0rVkcY'.format(latitude,longitude,pitch,head)
            urls.append({'long':longitude,'lat':latitude,'url':url})
        return urls

    def search_by_name(self,data): 
 
        address = data['name']
        geocode_result = gmaps.geocode(address)[0]
        geocode_result.keys()
        lat1=geocode_result['geometry']['location']['lat']
        lng1=geocode_result['geometry']['location']['lng']
        
        url=self.generate_image_urls(lng1,lat1)

        return [],url


    def search_bounding_box(self,data):
        """if name is specified, search the name in the bounding box, find corresponding street view images 
           return (dict{place name:{"longtitude":longtitude,"latitude":latitude,"information":information}},[image urls])
           if not, find all streetview images in the bounding box
           return (None,[image urls]"""

        """If no name, all images:"""
        temp=check_keys(data,['min_lat','max_lat','min_long','min_long'])
        if temp!=None:
            return ({temp+ " not found"},[])
        logging.info('begin running search_bounding_box')  
        values=[check_float(data[i],-180,180) for i in ["max_long",'min_long','max_lat','min_lat']]
        for v in values:
            if v==None:
                return ("invalid value",[])
        max_long,min_long,max_lat,min_lat=values    
        url="http://www.openstreetmap.org/api/0.6/map?bbox={},{},{},{}".format(min_long,min_lat,max_long,max_lat)
        
        #parse xml for lat and lng values
        urls=[]
        print "google"
        places=[]
        try:
            temp = urllib2.urlopen(url)
            dom=temp.read()
            i=0
            import re
            pattern1=re.compile('lat="-?[0-9]+.[0-9]+" lon="-?[0-9]+.[0-9]+"')
            pattern2=re.compile('-?[0-9]+.-?[0-9]+')
            for string in pattern1.findall(dom):
                latitude,longitude=[float(i) for i in pattern2.findall(string)]
                if longitude>=min_long and longitude<=max_long and latitude>=min_lat and latitude<=max_lat:
                    urls=urls+self.generate_image_urls(longitude,latitude)
        except urllib2.HTTPError,e:
            logging.info('This bounding box cannot be found on openstreetmap.org, please try other bounding box.')

        return urls
    
    def search_coordinate(self,data):
        
        temp=check_keys(data,['longitude','latitude'])
        if temp!=None:
            return ({temp+ " not found"},[])

        urls=[]
        for longitude,latitude in data:
            urls=urls+self.generate_image_urls(longitude,latitude)

        return [],urls

    def search_by_street(self,data):

        urls=[]
        for longitude,latitude in data:
            urls=urls+self.generate_image_urls(longitude,latitude)

        return [],urls
