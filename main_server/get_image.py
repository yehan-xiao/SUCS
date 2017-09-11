#Written by Shitao Tang
# --------------------------------------------------------
import requests,web,urllib,os
class Image:
    def GET(self, url):
        url=urllib.unquote(url)
        return requests.get(url).content


