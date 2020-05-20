#!/usr/bin/python

import mechanize
from bs4 import BeatifulSoup
import hashlib

br = mechanize.Browwser()
btr = br.open('docker.hackthebox.eu:32124')
bt = BeatifulSoup(btr)
md = bt.h3.get_text()
re = hashlib.md5(md.encode('utf-8')).hexdigest()
br.select_form(nr=0)
br.form['hash'] = re
br.submit()
print br.response().read()