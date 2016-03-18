import numpy as np

import csv
import json
'''
"Horse Name","Jockey","Odds","Last Raced","Place","Park","Date","Race Number"

Odds, place
'''
class getHorseData:
	csvPath = "../data/decryptedResultsData/resultsCSV/raceResults.csv"
	horseDataPath = "../data/decryptedResultsData/resultsCSV/horses.json"

	def __init__(self):
		pass
	
	def getCSVData(self):
		cf = open(self.csvPath, 'r')
		data = np.array(list(csv.reader(cf)))
		allData = np.delete(data, 0, 0)

		noNames = np.delete(allData, 0, 1)

		return allData, noNames

	def getJSONData(self):
		data = {}
		with open(self.horseDataPath) as f:
			data = json.load(f)

		master = [] #holds the final horse data to return
		masterNoSale = []

		positions = [] #holds the positions the horses came in in the raceData.csv
		positionsNoSale = []

		names = [] #holds the names of the horses corresponding to the row in master
		namesNoSale = []

		allRaceData, noNamesData = self.getCSVData() #get allRaceData to determine the position of the horse
		rdn, rdp = allRaceData.shape

		print "Creating data matrix"
		tracker = 0
		for horse in data['horses']:
			if ( ( not horse['lastPriceSold'] == "N/A" ) and ( horse['valid'] == 1 ) ):
				if (tracker == 777 or tracker == 1349):
					tracker+=1
					continue
				tracker += 1
				newRow = []
				newRow.append(float(horse['currentYear']['starts']))
				newRow.append(float(horse['currentYear']['firsts']))
				newRow.append(float(horse['currentYear']['seconds']))
				newRow.append(float(horse['currentYear']['thirds']))
				newRow.append(float(horse['currentYear']['earningsPerStart'].replace(',', '')))
				newRow.append(float(horse['career']['starts']))
				newRow.append(float(horse['career']['firsts']))
				newRow.append(float(horse['career']['seconds']))
				newRow.append(float(horse['career']['thirds']))
				newRow.append(float(horse['career']['earningsPerStart'].replace(',', '')))
				newRow.append(float(horse['lastPriceSold'].replace(',', '')))
				count = 0
				position = 0
				names.append(horse['name'])

				for workout in horse['workouts']:
					#count workouts
					count += 1
					#figure out average position in those workouts...default to 1
					p = float(workout['position'])
					oh = float(workout['otherHorses'])
					position += p/oh
				if (count == 0):
					position = 1
				else:
					position = float(position)/float(count)

				newRow.append(float(count))
				newRow.append(float(position))
				newRow.append(float(2016-int(horse['birthyear'])))
				master.append(newRow)

				for k in range(0, rdn):
					if(allRaceData[k][0] == horse['name']):
						positions.append(allRaceData[k][4]) #adds the horse's position to the position list
						break
			if ( horse['valid'] == 1  ):
				#TODO
				newRow = []
				newRow.append(float(horse['currentYear']['starts']))
				newRow.append(float(horse['currentYear']['firsts']))
				newRow.append(float(horse['currentYear']['seconds']))
				newRow.append(float(horse['currentYear']['thirds']))
				newRow.append(float(horse['currentYear']['earningsPerStart'].replace(',', '')))
				count = 0
				position = 0
				namesNoSale.append(horse['name'])

				for workout in horse['workouts']:
					#count workouts
					count += 1
					#figure out average position in those workouts...default to 1
					p = float(workout['position'])
					oh = float(workout['otherHorses'])
					position += p/oh
				if (count == 0):
					position = 1
				else:
					position = float(position)/float(count)

				newRow.append(float(count))
				newRow.append(float(position))
				newRow.append(float(2016-int(horse['birthyear'])))
				masterNoSale.append(newRow)

				for k in range(0, rdn):
					if(allRaceData[k][0] == horse['name']):
						positionsNoSale.append(allRaceData[k][4]) #adds the horse's position to the position list
						break
					if (k == rdn-1):
						print "couldn't find: %s" % horse['name']


		n,p = np.array(masterNoSale).shape

		return np.array(master), positions, names, np.array(masterNoSale), positionsNoSale, namesNoSale

		#TODO: remove all of the horses with important data missing...
			#e.g. auction price, workouts... 
			#want to remove the name of the horse...
		#return different versions of data...
			# - with the horses without auction price missing
			# - with the auction price variable missing
			# - with the total workouts... 0 for those without workouts
			# - with horses without workouts missing (holds performance in the workouts as percentage (1/49... 15/22... etc))
		#return these as matrices
'''
TODO:
- get one big matrix with comparable data:
for each horse:
	current year:
		starts, firsts, seconds, thirds, earnings per start
	career:
		starts, firsts, seconds, thirds, earnings per start
	auction price

'''


