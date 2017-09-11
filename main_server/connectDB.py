#Written by Shitao Tang, Yehan Xiao
# --------------------------------------------------------
import MySQLdb,logging
from config import conf
class database():
    instance=None
    def __init__(self):
        self.conn=None
        self.curs=None
        self.connect()

    @staticmethod
    def getInstance():
        if database.instance==None:
            database.instance=database()
        return database.instance
    
    def connect(self): #connect to a database
        try:
            self.conn= MySQLdb.connect(
                        host=conf.HOST,
                        port=conf.PORT,
                        user=conf.USERNAME,
                        passwd=conf.PASSWORD,
                        db =conf.DATABASE
                        )
            self.curs=self.conn.cursor()
        except MySQLdb.Error as err:
            logging.error('{}'.format(err))
    
    def create_account(self,username,password_md5): #create an account
        self.connect()
        sql1='SELECT * FROM account WHERE username="{}"'.format(username)
        sql2='INSERT INTO account VALUES("{}","{}")'.format(username,password_md5)
   
        try: 
            self.curs.execute(sql1)
            if len(self.curs.fetchall())!=0:
                return 'username already exists'
            self.curs.execute(sql2)
            return "Signup successfully"
        except MySQLdb.Error,e:
            try:
                logging.error("Mysql error [{}]:{}".format(e.args[0],e.args[1]))
            except IndexError:
                logging.error("Mysql error {}".format(str(e)))
            return 'Fail to signup'
        
    def authenticate_account(self,username,password_md5):
        self.connect()
        sql='SELECT * FROM account WHERE username="{}" and password_md5="{}"'.format(username,password_md5)
        try:
            self.curs.execute(sql)
            if len(self.curs.fetchall())!=0:
                return True
            else:
                return False
        except MySQLdb.Error,e:
           try:
               logging.error("Mysql error [{}]:{}".format(e.args[0],e.args[1]))
           except IndexError:
               logging.error("Mysql error {}".format(str(e)))
           return 'Fail to signup'
        
         
    def save_image_url(self,token,time,longitude,latitude,url): #save the image url to database
        self.connect()
        sql='INSERT INTO image_info VALUES("{}",{},{},{},"{}");'.format(token,time,longitude,latitude,url)
        try:
            self.curs.execute(sql)
	    self.conn.commit()
        except MySQLdb.Error,e:
            try:
                logging.error("Mysql error [{}]:{}".format(e.args[0],e.args[1]))
            except IndexError:
                logging.error("Mysql error {}".format(str(e)))
            
    def get_image_infos(self,token,time,limit): #get the image url and delete that from database
        self.connect()
        sql='SELECT longitude,latitude,url FROM image_info WHERE token="{}" and time={} LIMIT {}'.format(token,time,limit)
        sql1='DELETE FROM image_info where token="{}" and time = {} and longitude = {} and latitude = {} and url ="{}"'
        results=[]
        try:
            self.curs.execute(sql)
            res=self.curs.fetchall()
            for row in res:
                results.append({'long':float(row[0]),'lat':float(row[1]),'url':row[2]})
                self.curs.execute(sql1.format(token,time,row[0],row[1],row[2]))
		self.conn.commit()
        except MySQLdb.Error, e:
            try:
                logging.error("Mysql error [{}]:{}".format(e.args[0],e.args[1]))
            except IndexError:
                logging.error("Mysql error {}".format(str(e)))

        return results
         

    def remove_image_infos(self,token,time,image_infos): #remove a list of image urls from database
        sql='DELETE FROM image_info where token="{}" and time = "{}" and longitude = "{}" and latitude = "{}" and url ="{}"'

        try:
            for image_info in image_infos:
                latitude=image_info['lat']
                longitude=image_info['long']
                url=image_info['url']
                self.curs.execute(sql.format(token,time,longitude,latitude,url))
		self.conn.commit()
        except MySQLdb.Error,e:
            try:
                logging.error("Mysql error [{}]:{}".format(e.args[0],e.args[1]))
            except IndexError:
                logging.error("Mysql error {}".format(str(e)))

    def store_image_searched(self,image_md5s): #save image that has already been analysed
        self.connect()
        sql='INSERT INTO images VALUES("{}");'
        try:
            for image_md5 in image_md5s:
                self.curs.execute(sql.format(image_md5))
		self.conn.commit()
        except MySQLdb.Error, e:
            try:
                logging.error("Mysql error [{}]:{}".format(e.args[0],e.args[1]))
            except IndexError:
                logging.error("Mysql error {}".format(str(e)))

    
    def get_image_seaerched(self,image_md5): #check whether a image is analysed
        self.connect()
        sql='SELECT * FROM images WHERE image_md5="{}";'
        try:
            self.curs.execute(sql.format(image_md5))
            res=self.curs.fetchall()
            if len(res)!=0:
                return True
        except MySQLdb.Error, e:
            try:
                logging.error("Mysql error [{}]:{}".format(e.args[0],e.args[1]))
            except IndexError:
                logging.error("Mysql error {}".format(str(e)))

        return False

