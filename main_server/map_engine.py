#Written by Shitao Tang
# --------------------------------------------------------
class map:
    @staticmethod
    def getInstance():
        """get an instance"""
        pass

    def search_by_name(self,data):
        """search by the name and center. find corresponding street view images
        return (dict{place name:{"longtitude":longtitude,"latitude":latitude,"information":information}},[image urls])"""
        pass

    def search_bounding_box(self,data):
        """if name is specified, search the name in the bounding box, find corresponding street view images 
           return (dict{place name:{"longtitude":longtitude,"latitude":latitude,"information":information}},[image urls])
           if not, find all streetview images in the bounding box
           return (None,[image urls]"""
        pass

    def search_coordinate(self,data):
        """find information of the place and the corresponding street view
           return (dict{place name:information},image url)"""
        pass
