#!/usr/bin/python

import requests
from bs4 import BeautifulSoup
import hashlib
import sys

port = raw_input("Enter the intance port number : ")
url = 'http://docker.hackthebox.eu:'+ port
print "The target url is : " + url
request = requests.session()
response = request.get(url).content
response = BeautifulSoup(response,'html5lib')
response = response.h3.get_text()
mdhash = hashlib.md5(response.encode('utf-8')).hexdigest()
flag = request.post(url=url, data= dict(hash=mdhash))
flag = BeautifulSoup(flag.text,'html5lib')
flag = flag.p.get_text()
print "The flag is : " + flag
