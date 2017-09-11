#Written by Shitao Tang
# --------------------------------------------------------
import web
import logging
import __init__
import sys

from ucs_server import UCS
from baidu import baidu
from config import conf
from get_image import Image
urls = (
    '/UCS', 'UCS',
    '/index','index',
    '/image/(.*)','Image',

)
if __name__ == "__main__": 
    reload(sys)
    sys.setdefaultencoding('utf8')
    web.config.debug=False
    logging.info("UCS starting...")
    app = web.application(urls, globals())
    session = web.session.Session(app, web.session.DiskStore('sessions'),initializer={'token': None,'search_time':0,'map_engine':conf.BAIDU})
    web.config._session=session
    app.run()
