import PyPDF2 as pdf
import csv
import unicodedata
import re

class equibasePdfScraper:
	#vars:
	oddsPattern = re.compile('[0-9]*\.[0-9][0-9]')

	def __init__(self):
		pass
		
	#checks if odds are valid
	def isValidOdds(self, oddsStr):
		oddsFloat = float(oddsStr)
		valid = 1
		if (oddsFloat > 150):
			valid = 0
		return valid

	def makeValidOdds(self, oddsStr):
		validOdds = oddsStr
		while (len(validOdds) > 5):
			validOdds = validOdds[1:]
		return validOdds

	def getParkAndDate(self, line):
		print line
		park = 1
		t_park = ""
		t_date = ""
		for c in line:
			if(park):
				if(c != '-'):
					t_park += c
				else:
					park = 0
					continue
			else:
				if(c != '-'):
					t_date += c
				else:
					break
		print t_park
		print t_date
		return t_park, t_date



		return "March 3rd"


	def parse(self, pdfs, outputFile):
		nPdfs = len(pdfs)
		for k in range(0, nPdfs):
			pdfdoc = open(pdfs[k], 'rb')
			pdfReadable = pdf.PdfFileReader(pdfdoc)

			data = [[]]
			if (k == 0):
				data.append(["Horse Name", "Jockey", "Odds", "Last Raced", "Place", "Park", "Date", "Race Number"])
			raceDate = ""
			park = ""
			raceDateRetrieved = 0

			nPages = pdfReadable.getNumPages()
			for i in range(0, nPages):
				page = pdfReadable.getPage(i)
				pageText = page.extractText()

				#iterate thru lines of the pdf...
				#...grabbing appropriate values and adding to lists (each list would correspond to a row)

				lineCount = 0
				startFound = 0
				horseCount = 1
				oddsCount = 0
				lastRaced = []
				horsename = []
				jockey = []
				#start = []
				odds = []
				place = []
				race = []
				date = []
				parks = []

				for line in pageText.split('\n'):
					line = unicodedata.normalize('NFKD', line).encode('ascii','ignore')
					#get the race date on the first page
					if(i == 0 and raceDateRetrieved == 0):
						park, raceDate = self.getParkAndDate(line)
						raceDateRetrieved = 1

					if (startFound):
						lineCount += 1
						
						if (lineCount == 1):
							if(line[0].isdigit() or line[0] == '-'):
								if (line[0] == '-'):
									#sets lastRaced value to empty
									lastRaced.append("")

									#removes the dashes for the lack of date and continues with the same horse/jockey code
									line = line[3:]
									temphorse = ""
									tempjockey = ""
									horse = 1
									for c in line:
										if (c != '(' and not c.isdigit() and horse):
											temphorse += c
										elif(c == '('):
											horse = 0
										elif(c != ')'):
											if (not c.isdigit()):
												tempjockey += c
										else:
											jockey.append(tempjockey)
											horsename.append(temphorse)
											race.append(i)
											place.append(horseCount)
											date.append(raceDate)
											parks.append(park)
											horseCount += 1
											break
								else:
									lastRaced.append(line)
							else: 
								break

						#the horse and jockey:
						elif ("(" in line):
							temphorse = ""
							tempjockey = ""
							horse = 1
							for c in line:
								if (c != '(' and not c.isdigit() and horse):
									temphorse += c
								elif(c == '('):
									horse = 0
								elif(c != ')'):
									if (not c.isdigit()):
										tempjockey += c
								else:
									jockey.append(tempjockey)
									horsename.append(temphorse)
									race.append(i)
									place.append(horseCount)
									date.append(raceDate)
									parks.append(park)
									horseCount += 1
									break

						#the odds line
						if ("." in line):
							oddsMatch = self.oddsPattern.search(line)
							if (oddsMatch and oddsCount <= horseCount):
								oddsMatchStr = oddsMatch.group(0)
								if(self.isValidOdds(oddsMatchStr)):
									odds.append(oddsMatchStr)
								else:
									oddsMatchStr = self.makeValidOdds(oddsMatchStr)
									odds.append(oddsMatchStr)
								lineCount = 0
								oddsCount += 1


							#found the start of the table
						#the last raced line:
					if ("LastRacedPgmHorseName" in line):
						startFound = 1


				length = len(lastRaced)
				for i in range(0, length):
					tempRow = []
					
					tempRow.append(horsename[i])
					tempRow.append(jockey[i])
					tempRow.append(odds[i])
					tempRow.append(lastRaced[i])
					tempRow.append(place[i])
					tempRow.append(parks[i])
					tempRow.append(date[i])
					tempRow.append(race[i])
					
					data.append(tempRow)


			#put the lists into the csv
			#...row by row
			myfile = open(outputFile, 'a+')
			wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
			for mylist in data:
				wr.writerow(mylist)
			myfile.close()

			pdfdoc.close()

