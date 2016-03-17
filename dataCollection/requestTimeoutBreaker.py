import json
import os
import requests
import urllib2
from bs4 import BeautifulSoup
import pandas as pd
import time
import lxml.html
import re

class collectImageData:

	urlPattern = re.compile("<img src=\"(http://www\.equibase\.com/premium/eqbCaptcha\.cfm\?cp=.+)\" data-pin-nopin=")

	def __init__(self,content):
		print "collecting image in breakTimoutMechanism..."
		self.getImageURL(content)
		self.saveImage(content)

	def getImageURL(self,content):
		print "CONTENT:"
		myfile = open("testFile.txt", 'a+')
		myfile.write("CONTENT: POOP:")
		myfile.write(content)
		myfile.close()
		imageURL = self.urlPattern.search(content).group(1)
		print imageURL

	def saveImage(self,content):
		pass
