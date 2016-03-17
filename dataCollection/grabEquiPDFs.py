from equibasepdfScraper import equibasePDFparser
import sys
import requests
import urllib2
from bs4 import BeautifulSoup
import re

import time
import os.path


class PDFGrabber:
	#urls
	equibaseUrl = "http://www.equibase.com"
	equihome = "http://www.equibase.com/homehorseplayer.cfm"
	equiresults = "http://www.equibase.com/static/chart/pdf/index.html?SAP=TN"

	#regex
	linkPattern = re.compile('<a.+>[0-9][0-9]?</a>')
	hrefPattern = re.compile('href=\".+\"')
	urlPattern = re.compile('/.+\.html')
	pdfLink1Pattern = re.compile('href=\"/premium/chartEmb\.cfm.+\">')
	trackPattern = re.compile('track=.+&r')
	countryPattern = re.compile('&cy=.+')

	def __init__(self):
		resultsPage = self.grabPage(self.equiresults)

		#retrieves links for every track, every race
		links = self.souping(resultsPage)
		#now must retrieve the pdf on each

		for link in links:
			pdfPage = self.grabPage(self.equibaseUrl + link)
			pdfPagehtml = pdfPage.read()
			pdfLink = self.grabPdfLink(pdfPagehtml)

			pdfPage2 = self.grabPage(pdfLink)

			#the link to the actual .pdf file:
			pdfLinkFinal = self.createPdfLink(pdfLink)
			self.downloadPdf(pdfLinkFinal)
			#print pdfPage2
			#pdfPage2html = pdfPage2.read()
			#print pdfPage2html


			#self.downloadPdf()

		#creates an instance of equibase PDF parser
		#p = equibasePDFparser()
		#p.parse([sys.argv[1]], sys.argv[2])
	def downloadPdf(self, link):
		if (os.path.isfile("../data/" + link[41:])):
			print "../data/" + link[41:] + " already exists...skipping"
		else:
			print "waiting to connect..."
			time.sleep(30)
			print "attempting to connect to: " + link + "..."
			try:
				u = urllib2.urlopen(link)
				localFile = open("../data/" + link[41:], 'w+')
				localFile.write(u.read())
				localFile.close()
				print "wrote to: " + "../data/" + link[41:]
			except urllib2.HTTPError, e:
			   print "http err"
			except urllib2.URLError, e:
				print "url except"

	def createPdfLink(self, pdfLink):
		numbers = ""
		for c in pdfLink:
			if (c.isdigit()):
				numbers = numbers + c
		numbers1 = numbers[0:4]
		numbers2 = numbers[6:]
		dateStr = numbers1 + numbers2
		
		trackChunk = self.trackPattern.search(pdfLink).group(0)
		trackStr = trackChunk[6:]
		trackStr = trackStr[:len(trackStr)-2]

		countryChunk = self.countryPattern.search(pdfLink).group(0)
		countryStr = countryChunk[4:]

		return self.equibaseUrl + "/static/chart/pdf/" + trackStr + dateStr + countryStr + ".pdf"





	def grabPdfLink(self, pagehtml):
		htmlString = str(pagehtml)
		relLinkElem = self.pdfLink1Pattern.search(htmlString)
		rawlinkStr = relLinkElem.group(0)
		pureLinkStr = rawlinkStr[6:]
		pureLinkStr = pureLinkStr[0:len(pureLinkStr) - 2]
		return self.equibaseUrl + pureLinkStr


	def souping(self, page):
		soup = BeautifulSoup(page, "lxml")		
		soup.prettify()
		table = soup.find_all('table')
		linksRaw = self.extractTableLinks(table)
		return linksRaw

	def extractTableLinks(self, table):
		links = table[1].find_all('a')
		data = []
		for link in links:
			temp_link = str(link)
			linkRelevent = self.linkPattern.search(temp_link)
			if (linkRelevent):
				hrefRelevent = self.hrefPattern.search(linkRelevent.group(0))
				urlRelevent = self.urlPattern.search(hrefRelevent.group(0))
				data.append(urlRelevent.group(0))
		return data


	def grabPage(self, source):
		req = urllib2.Request(source)
		page = urllib2.urlopen(req)
		return page

		

p = PDFGrabber()