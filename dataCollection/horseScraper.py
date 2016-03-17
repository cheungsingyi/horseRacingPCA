import json
import requests
import urllib2
from bs4 import BeautifulSoup
import pandas as pd
import time
import lxml.html
import re
from xml.etree import ElementTree

import sys
import os

from proxyHandler import proxyRequest

class horseScraper:
	csvPath = "/Users/markusnotti/Documents/UCLA/Winter2016/170A-Mathmatical Modeling and Methods for Computer Science/horseRacing/data/decryptedResultsData/resultsCSV/raceResults.csv"
	horseDataPath = "/Users/markusnotti/Documents/UCLA/Winter2016/170A-Mathmatical Modeling and Methods for Computer Science/horseRacing/data/decryptedResultsData/resultsCSV/horses.json"
	equibaseHomeUrl = "http://www.equibase.com/"
	equibaseHorseBaseUrl = "http://www.equibase.com/profiles/Results.cfm?type=Horse"

	#regex
	horseLinkPattern = re.compile("profiles/Results\.cfm\?type=Horse&refno=[0-9]+&registry=T\'>.+</a></td>\s+<td >[0-9][0-9][0-9][0-9]")
	horseSearchPattern = re.compile("Horse Search")
	horseProfilePattern = re.compile("Horse Profile")
	refinePattern = re.compile(".+registry=T")
	foaledPattern = re.compile("foaled ([a-zA-Z]+) [0-9]+, ([0-9]+)</p>") 

	workoutDataPattern = re.compile("<td class=\"workoutTableHeader\" style=\"width:10%; text-align:center;\">Rank</td>.+Includes workouts from the last 60 days", re.DOTALL)
	workoutRowsPattern = re.compile("<tr>(.+?)</tr>", re.DOTALL)
	workoutTableDataPattern = re.compile("<td class=\"\" style=\"text-align:[a-z]+;\">(.+?)</td", re.DOTALL)
	workoutTrackPattern = re.compile("/profiles/Results.cfm\?.+>(.+)</a>")
	workoutPositionPattern = re.compile("([0-9]+)/([0-9]+)")
	
	careerPattern = re.compile("<div id=\"career\" class=\"profileStatsColumn\">.+Earnings Per Start: \$[0-9,]+", re.DOTALL)
	currentYearPattern = re.compile("<div id=\"currentYear\" class=\"profileStatsColumn\">.+Earnings Per Start: \$[0-9,]+", re.DOTALL)
	auctionHistoryPattern = re.compile("<div class=\"tab-pane\" id=\"salesHistory\".+?\$([0-9,]+)", re.DOTALL)

	csp = re.compile("Starts: ([0-9]+)")
	cfp = re.compile("Firsts: ([0-9]+)")
	csecp = re.compile("Seconds: ([0-9]+)")
	ctp = re.compile("Thirds: ([0-9]+)")
	cepsp = re.compile("Earnings Per Start: \$([0-9,]+)")

	horseNotSoldAtAuctionPattern = re.compile("This horse has not been sold via public auction")
	tooManyRequestsPattern = re.compile("The custom error module does not recognize this error\.")



	def __init__(self):
		self.requestDelay = float(sys.argv[1])
		self.ph = proxyRequest()

		scrapedCount = 0
		names = self.getHorseNames()
		for name in names:
			if (self.jsonContainsHorse(name)):
				print "json contains %s...skipping to next horse" % name
				continue
			print "waiting to scrape %s" % name
			time.sleep(self.requestDelay)
			print "commencing scrape of %s" % name
			self.searchAndScrapeHorse(name)
			scrapedCount += 1
			print "horses scraped = %d " % scrapedCount



	def writeToHorses(self, obj):
		with open(self.horseDataPath) as horseDataFile:
			self.horseData = json.load(horseDataFile)
		self.horseData['horses'].append(obj)
		with open(self.horseDataPath, 'w+') as outfile:
			json.dump(self.horseData, outfile, indent=4, separators=(',',': '))
		print "%s written to %s" % (obj['name'], self.horseDataPath)
			
	def searchAndScrapeHorse(self, name):
		p = {
				"searchVal":"horses",
				"horse_name": name
			}

		print "Waiting to get horse search results..."
		time.sleep(self.requestDelay)
		print "attempting to connect via proxy (post)..."
		content = self.ph.postRequest(self.equibaseHorseBaseUrl,p)
		#r = requests.post(self.equibaseHorseBaseUrl,p)
		#content = r.content
		if (self.tooManyRequestsPattern.search(content)):
			print "TOO MANY REQUESTS ERROR...FIX AND RESTART SCRAPE"
		if (not self.foundHorse(content)):
			#gets right link for horse, if profile cannot be found, prints error and returns
			content,err = self.getHorseProfile(content, name)
			if(err):
				print "ERROR: could not find profile for %s" % name
				return

		#continue and scrape page
		try:
			self.scrapeHorseProfile(content, name)
		except:
			pass

	def getHorseProfile(self, c, name):
		for match in re.findall(self.horseLinkPattern, c):
			birthyear = int(match[len(match) - 4:])
			if (birthyear > 2006):
				url = self.refinePattern.search(match).group(0)
				print "waiting to navigate to horse profile..."
				time.sleep(self.requestDelay)
				print "attempting to use proxy..."
				content = self.ph.getRequest(self.equibaseHomeUrl + url)
				#r = requests.get(self.equibaseHomeUrl + url)
				if (self.tooManyRequestsPattern.search(content)):
					print "TOO MANY REQUESTS ERROR...FIX AND RESTART SCRAPE"
					return content, 1
				print "valid birthyear"
				return content, 0
			else:
				print "invalid birthyear"
				continue
		#if it can't find profile due to too many requests error
		if (self.tooManyRequestsPattern.search(c)):
			print "TOO MANY REQUESTS ERROR...FIX AND RESTART SCRAPE"
			return c, 1

		#could not find appropriate horse profile for search...returns err
		self.createEmptyHorseJSON(name)
		return c, 1


	def scrapeHorseProfile(self, content, name):

		#COMMENCE THE REGEX!!!
		rawFoaledDate = self.foaledPattern.search(content).group(0)[7:len(self.foaledPattern.search(content).group(0)) - 4]
		foaledMonth = self.foaledPattern.search(content).group(1)
		foaledYear = self.foaledPattern.search(content).group(2)
		career = self.careerPattern.search(content).group(0)
		careerStarts = self.csp.search(career).group(1)
		careerSeconds = self.csecp.search(career).group(1)
		careerFirsts = self.cfp.search(career).group(1)
		careerThirds = self.ctp.search(career).group(1)
		careerEarningsPerStart = self.cepsp.search(career).group(1)

		currentYear = self.currentYearPattern.search(content).group(0)
		currentStarts = self.csp.search(currentYear).group(1)
		currentSeconds = self.csecp.search(currentYear).group(1)
		currentFirsts = self.cfp.search(currentYear).group(1)
		currentThirds = self.ctp.search(currentYear).group(1)
		currentEarningsPerStart = self.cepsp.search(currentYear).group(1)


		#for each row collect the table:


		lastPriceSold = ""
		if(self.horseSoldAtAuction(content)):
			if(self.auctionHistoryPattern.search(content)):
				lastPriceSold = self.auctionHistoryPattern.search(content).group(1)
			else:
				print "Check auction history for: %s" % name
				lastPriceSold = "N/A"
		else:
			lastPriceSold = "N/A"

		#PRINT LOTS OF STUFF
		'''
		print "printing data collected for: %s" % name
		print "foaled:"
		print rawFoaledDate
		print foaledMonth
		print foaledYear

		print "career:"
		print careerStarts
		print careerFirsts
		print careerSeconds
		print careerThirds
		print careerEarningsPerStart

		print "currentYear: "
		print currentStarts
		print currentFirsts
		print currentSeconds
		print currentThirds
		print currentEarningsPerStart

		print "last sold at:"
		print lastPriceSold
		'''

		#ASSEMBLE THE HORSE OBJECT!
		horseObj = {}
		horseObj['name'] = name
		horseObj['valid'] = 1
		horseObj['birthmonth'] = foaledMonth
		horseObj['birthyear'] = foaledYear
		horseObj['career'] = {
			'starts' : careerStarts,
			'firsts' : careerFirsts,
			'seconds' : careerSeconds,
			'thirds' : careerThirds,
			'earningsPerStart' : careerEarningsPerStart
		}
		horseObj['currentYear'] = {
			'starts' : currentStarts,
			'firsts' : currentFirsts,
			'seconds' : currentSeconds,
			'thirds' : currentThirds,
			'earningsPerStart' : currentEarningsPerStart
		}
		horseObj['lastPriceSold'] = lastPriceSold
		horseObj['workouts'] = []


		#workout data
		if(self.workoutDataPattern.search(content)):
			workoutTable = self.workoutDataPattern.search(content).group(0)
			workoutRows = self.workoutRowsPattern.findall(workoutTable)
			for row in workoutRows:
				workoutRowData = self.workoutTableDataPattern.findall(row)
				rowObj = {}
				rowData = []
				i = 0
				for data in workoutRowData:
					if(i == 0):
						#special regex to get the name of the track
						if(self.workoutTrackPattern.search(data)):
							rowData.append(self.workoutTrackPattern.search(data).group(1))
						else:
							rowData.append("N/A")
					elif(i == 6):
						#special regex to get the position and the amount of other horses in the workout
						rowData.append(self.workoutPositionPattern.search(data).group(1))
						rowData.append(self.workoutPositionPattern.search(data).group(2))
					else:
						#append what was captured with the OG regex...
						rowData.append(data)
					i += 1

				rowObj['track'] = rowData[0]
				rowObj['date'] = rowData[1]
				rowObj['type'] = rowData[2]
				rowObj['distance'] = rowData[3]
				rowObj['time'] = rowData[4]
				rowObj['notes'] = rowData[5]
				rowObj['position'] = rowData[6]
				rowObj['otherHorses'] = rowData[7]

				horseObj['workouts'].append(rowObj)

		#finally write the assmebled json obj to the horse.json file
		self.writeToHorses(horseObj)

	def createEmptyHorseJSON(self, name):
		horseObj = {}
		horseObj['name'] = name
		horseObj['valid'] = 0
		horseObj['birthmonth'] = "N/A"
		horseObj['birthyear'] = "N/A"
		horseObj['career'] = {
			'starts' : "N/A",
			'firsts' : "N/A",
			'seconds' : "N/A",
			'thirds' : "N/A",
			'earningsPerStart' : "N/A"
		}
		horseObj['currentYear'] = {
			'starts' : "N/A",
			'firsts' : "N/A",
			'seconds' : "N/A",
			'thirds' : "N/A",
			'earningsPerStart' : "N/A"
		}
		horseObj['lastPriceSold'] = "N/A"
		horseObj['workouts'] = []
		self.writeToHorses(horseObj)


	def horseSoldAtAuction(self, content):
		if (self.horseNotSoldAtAuctionPattern.search(content)):
			return 0
		else:
			return 1

	def foundHorse(self, content):
		found = 0
		if(self.horseSearchPattern.search(content)):
			found = 0
			print "search"
		elif(self.horseProfilePattern.search(content)):
			found = 1
			print "profile"
		return found


	def getHorseNames(self):
		f = pd.read_csv(self.csvPath)
		names = f['Horse Name']
		return names

	def jsonContainsHorse(self, name):
		with open(self.horseDataPath) as horseDataFile:
			self.horseData = json.load(horseDataFile)
		for horse in self.horseData['horses']:
			if(horse['name'] == name):
				return 1
		return 0

	def initializeJSONFile(self):
		newObj = {'horses': []}
		with open(self.horseDataPath, 'w+') as outfile:
			json.dump(newObj, outfile, indent=4, separators=(',',': '))
		print "JSON file initialized to %s" % (obj['name'], self.horseDataPath)




test = horseScraper()
