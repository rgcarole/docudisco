import httplib2
import json
import datetime
import base64
import sys
import os
import getpass
import errno
import urllib
import urllib2

from urllib2 import urlopen
from json import dumps

from socket import error as socket_error
import socket

apiMethod="https://"
apiVersion="/v22"
apiServer="api.weaved.com"
apiKey="WeavedDemoKey$2015"

#===============================================
if __name__ == '__main__':

    httplib2.debuglevel     = 0
    http                    = httplib2.Http()
    content_type_header     = "application/json"

    userName = "rcarole@gmail.com" 
    password = "password"
    URL = "" 
   
    loginURL = apiMethod + apiServer + apiVersion + "/api/user/login"

    loginHeaders = {
                'Content-Type': content_type_header,
                'apikey': apiKey
            }
    try:        
        response, content = http.request( loginURL + "/" + userName + "/" + password,
                                          'GET',
                                          headers=loginHeaders)
    except:
        print "Server not found.  Possible connection problem!"
        exit()                                          
#    print (response)
#    print "============================================================"
#    print (content)
#    print

    try: 
        data = json.loads(content)
        if(data["status"] != "true"):
            print "Can't connect to Weaved server!"
            print data["reason"]
            exit()

        token = data["token"]
    except KeyError:
        print "Comnnection failed!"
        exit()
        
    print "Token = " +  token

deviceListURL = apiMethod + apiServer + apiVersion + "/api/device/list/all"
content_type_header     = "application/json"

deviceListHeaders = {
                'Content-Type': content_type_header,
                'apikey': apiKey,
                # you need to get token from a call to /user/login
                'token': token,
            }

if __name__ == '__main__':            
    httplib2.debuglevel     = 0
    http                    = httplib2.Http()

    response, content = http.request( deviceListURL,
                                          'GET',
                                          headers=deviceListHeaders)
#    print content

    try:
        data = json.loads(content)
        if(data["status"] != "true"):
            print "Can't connect to Weaved server!"
            print data["reason"]
            exit()

        UID = data["devices"][0]["deviceaddress"]
    except KeyError:
        print "Comnnection failed!"
        exit()

    print "UID = " +  UID


def proxyConnect(UID, token):
    httplib2.debuglevel     = 0
    http                    = httplib2.Http()
    content_type_header     = "application/json"

  # this is equivalent to "whatismyip.com"
    my_ip = urlopen('http://ip.42.pl/raw').read()
    proxyConnectURL = apiMethod + apiServer + apiVersion + "/api/device/connect"

    proxyHeaders = {
                'Content-Type': content_type_header,
                'apikey': apiKey,
                'token': token
            }

    proxyBody = {
                'deviceaddress': UID,
                'hostip': my_ip,
                'wait': "true"
            }

    response, content = http.request( proxyConnectURL,
                                          'POST',
                                          headers=proxyHeaders,
                                          body=dumps(proxyBody),
                                       )
    try:
        data = json.loads(content)["connection"]["proxy"]
        return data
    except KeyError:
        print "Key Error exception!"
        print content
   
if __name__ == '__main__':
	URL = proxyConnect(UID, token)

print "URL = " + URL

c_url = URL
data = '{"type":"customer.card.created"}'
req = urllib2.Request(c_url, data)
#response = urllib2.urlopen(req)
