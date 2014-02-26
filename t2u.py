# -*- coding: utf-8 -*-
#!/usr/bin/env python
############################
# 
#  推你 For Alfredworkflow
#
#  __author__ = 'jack'
############################
__author__ = 'jack'

import os
import urllib,urllib2
from Feedback import Feedback
import time
import json
import base64
import sys

#中文乱码
reload(sys)
sys.setdefaultencoding( "utf-8" )

url = "http://t2u.me/t3/api/open/openTransfer"
appID = "c816f347bd024aa9292781449d1e5fe6"
accessToken = "ac4b1deaf05b2f2a3a51ab14cee218b6"

def log_out(content):
    fname = './debug.txt'
    try:
        fobj = open(fname, 'a')
    except IOError, e:
        print "file open error", e
    else:
        txts = []
        txts.append(content)
        fobj.writelines(['%s%s' % (x, os.linesep) for x in txts])
        fobj.close()

def post(data):
    if data is None:
        return
    data = urllib.urlencode(data)
    request = urllib2.Request(url, data)
    response = urllib2.urlopen(request)
    return response.read()

def getCurrentTime():
    return time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))

def process(alfred_data):
    #log_out(json.dumps(alfred_data))
    tNumberOrName = alfred_data['id']
    transferPasswd = alfred_data['passwd']
    tContent = alfred_data['content']

    time = getCurrentTime()
    lang = "en"
    source = "2001"
    params = {"appID":appID, "accessToken":accessToken, "tNumberOrName":tNumberOrName, "transferPasswd":transferPasswd, "tContent":tContent}
    jparams = json.dumps(params)
    ret = base64.encodestring(jparams)
    sign = None
    data = {"time":time, "lang":lang, "source":source, "param":ret, "sign":sign}
    resp = post(data)
    result = json.loads(resp)
    code = result['code']
    if code == '101':
        value = result['value']
        msg = value['msg']
        failedTransferList = value['failedTransferList']
        rt = msg
        if len(failedTransferList) > 0:
            rt += u": "
            rt += ";".join(failedTransferList)
        return rt
    else:
        return result['message']


