# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 09:31:41 2016

@author: Mz
"""

import urllib2
from bs4 import BeautifulSoup
import re
import cookielib
from cookielib import CookieJar
import time

cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent', 'Mozilla/5.0')]

def main():
    