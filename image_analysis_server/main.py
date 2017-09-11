#Written by Shitao Tang
# --------------------------------------------------------
import web
import logging
import logging.config
import detect
from connection_ok import connection
urls = (
    '/detect/(.*)', 'detect.detect',
    '/ok','connection'
)
if __name__ == "__main__": 
    logging.info('Starting image analysis server...')
    app = web.application(urls, globals())
    app.run()
