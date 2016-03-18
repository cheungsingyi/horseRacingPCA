import numpy as np
from toUsableData import getHorseData
import matplotlib.pyplot as plt
import matplotlib as mpl
import scipy

class analyze:
	colors = [	'yellow', 'silver', 'brown', 
			'red', 'red', 'red', 'red', 
			'red', 'red', 'red', 'red', 
			'red', 'red', 'red', 'red', 
			'red'	]

	levels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]


	def __init__(self):
		dataSource = getHorseData()
		self.raceData, self.raceDataNoNames = dataSource.getCSVData()
		self.horseData, self.positions, self.names, self.horseDataNoSale, self.positionsNoSale, self.namesNoSale = dataSource.getJSONData()

	def corr(self, X):
		#return the correlation matrix of X
		n,m = X.shape
		M = self.findM(X)
		S = self.findS(X)
		Z = np.divide((X - M), S)
		R = (float(1)/float(n)) * np.array(np.dot(np.transpose(Z), Z))
		#f = open("corr.txt", 'w+')
		#R.tofile(f, sep="", format="%s")
		#f.close()
		return R

	def normalize(self, X):
		n,m = X.shape
		M = self.findM(X)
		S = self.findS(X)
		Z = np.divide((X - M), S)
		return Z

	def cov(self, X):
		#return the covariance matrix of X
		n,m = X.shape
		M = self.findM(X)
		C =  (float(1)/float(n-1)) * np.array(np.dot(np.transpose(X - M), (X - M)))
		return C

	def PCA(self, X, type):
		#return first three principal components - p1, p2, p3
		#if type == corr: use corr
		#if type == cov: use cov
		X = np.array(X)
		svdTarget = np.array([])
		if(type == "corr"):
			svdTarget = self.corr(X)
		elif(type == "cov"):
			svdTarget = self.cov(X)
		else:
			print "ERROR: third arg should be \'corr\' or \'cov\'"
		U, s, V = np.linalg.svd(svdTarget)
		return U[:,[0]], U[:,[1]], U[:,[2]]

	def findM(self, X):
		#finds the column means and stacks to the dimensions of X
		#returns M
		#used to find the correlation matrix
		X = np.array(X)
		n,m = X.shape
		mu = np.mean(X, axis=0)
		M = np.ones((n, 1)) * mu 
		return M

	def findS(self, X):
		#finds the column stdevs and stacks to the dimensions of X
		#returns S
		#used to find the correlation matrix
		X = np.array(X)
		n,m = X.shape
		sigma = np.std(X, axis=0)
		S = np.ones((n, 1)) * sigma
		return S

	def scatterPlot(self, X, Y, xlabel, ylabel, title):
		#plots y against x
		#labels y and x
		plt.scatter(X, Y)
		plt.xlabel(xlabel)
		plt.ylabel(ylabel)
		plt.axis([np.amin(X) - 0.1, np.amax(X) + 0.1, np.amin(Y) - 0.1, np.amax(Y) + 0.1])
		plt.title(title)
		plt.show()

	def linearRegression(self, X, Y, xlabel, ylabel):
		#scatterPlots and draws the least squares linear regression
		pass

	def plotAllColumns(self, X):
		#takes all columns and plots them against each other
		X = np.array(X)
		n,p = np.shape(X)
		for i in range(0, p):
			for j in range(0, p):
				k = (j + 1) + (p * i)
				plt.subplot(p, p, k)
				plt.scatter(X[:,j], X[:,i])
				plt.axis([np.amin(X[:,j]) - 1, np.amax(X[:,j]) + 1, np.amin(X[:,i]) - 1, np.amax(X[:,i]) + 1])
				xlabel = "column %d" % j
				ylabel = "column %d" % i

				plt.xlabel(xlabel)
				plt.ylabel(ylabel)
		plt.show()

	def meansStdsOddsPositions(self):
		n,p = self.raceDataNoNames.shape
		X = test.raceDataNoNames[:,[1,3]].astype(float)

		means = [0 for m in range(0,14)]
		sigmas = [0 for s in range(0,14)]

		organized = [	[], [], 
						[], [], 
						[], [], 
						[], [],
						[], [],
						[], [],
						[], [],
						[]]

		for i in range(0,n):
			organized[int(X[i][1])].append(X[i][0])

		organized = np.array(organized)
		for i in range(0,14):
			means[i] = np.mean(organized[i+1])
			sigmas[i] = np.std(organized[i+1])

		return means, sigmas




'''
Ideas
1. CAN ODDS PREDICT OUTCOME?
	- Plot Position vs. Odds
		- Do the best odds mean the best chance?
		- Or is it something a little less expected?
		- Least Squares to determine if there is a trend
		- find the covariance
	- Average Odds of winning horses
	- Average Odds of placing horses

2. MAKE AN IMAGE WITH 3X3 PLOTS ( position, jockey, odds )
	- for every track
	- if any seem to show correlation...
		- solve least squares curve, r^2
	- make a covariance/correlation matrix for this as well

3. For the horses with workout data:
	- Plot every possible column:
		- last price sold ( if horse has it, include... )
		- age
		- birthmonth
		- career:
			- first
			- seconds
			- thirds
			- starts
			- earnings per start
		- current year: 
			- firsts
			- seconds
			- thirds
			- starts
			- earnings per start
		- name:
			- name length?
			- words in name? (search by capital letters?)
		- number of workouts in the last 60 days
		- workout performance:
			- average position amongst other horses

Helpful pages in the course reader:
155 - Solving Least Squares in Practice using SVD
162, 163 - Solving Least squares for a linear regression... also finding the covariance
175, 176 - Covariance
179 - correlation


'''


#plots odds v position


test = analyze()
xlabel = 'Position'
ylabel = 'Odds'
X = test.raceDataNoNames[:,[1,3]].astype(float)

plt.scatter(X[:,1], X[:,0])
plt.xlabel(xlabel)
plt.ylabel(ylabel)
plt.title("Odds v. Finishing Position")
plt.show()


#print test.findS(Y)
#print test.corr(X)
#print test.PCA(X, 'cov')
#test.plotAllColumns(Y)

#####################
#Least Squares of Odds v. Position (means and sigmas)
#####################

test = analyze()
means, sigmas = test.meansStdsOddsPositions()

A = np.ones((14, 2))
b = np.ones((14, 1))

for i in range(0, 14):
	A[i][0] = i + 1
	A[i][1] = 1
	b[i][0] = means[i]

z = np.dot(np.dot(np.linalg.inv(np.dot(A.T, A)),A.T), b)

regressY = []
for i in range(0,14):
	regressY.append(i*z[0][0] + z[1][0])

X = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
plt.plot(X, regressY, c = [1, 0, 0])
plt.scatter(X, means, c=[1, 0, 0])
plt.scatter(X, sigmas, c=[0, 1, 0])
xlabel = "Position"
ylabel = "Average Odds"
title = "Average Pre-Race Odds vs. Final Position"
plt.xlabel(xlabel)
plt.ylabel(ylabel)
plt.title(title)
plt.show()


######################
######################
######################




######################
#FIRST PCA ATTEMPT WITH 
#cyStarts,cyFirsts,cySeconds,cyThirds,cyEps,cStarts,cFirsts,cSeconds,cThirds,
#cEps,Price,nWorkouts,AvgPos,Age
#####################

test = analyze()
a,b,c = test.PCA(test.horseData, "corr")
print "First PC: \n%s\n" % a
print "Second PC: \n%s\n" % b
a = -1 * a
print "First PC flipped: \n%s\n" % a
n, p = test.horseData.shape
ab = np.column_stack((a.flatten(), b.flatten()))
x = []
y = []
normalizedHorses = test.normalize(test.horseData)
for i in range(0, n):
	temp = np.dot(normalizedHorses[i], ab)
	x.append(temp[0]) # PC 1
	y.append(temp[1]) # PC 2


cmap, norm = mpl.colors.from_levels_and_colors(levels=test.levels, colors=test.colors, extend='max')
plt.scatter(x,y,c=test.positions, edgecolor='none', cmap=cmap, norm=norm)
xlabel = "PC 1 - Career Starts, 1sts, 2nds, 3rds"
ylabel = "PC 2 - Career EPS, Current Year EPS"
title = "PCA 1 - Individual Horse Statistics"
plt.xlabel(xlabel)
plt.ylabel(ylabel)
plt.title(title)
plt.show()

################
################

#############################
#HALVING THE DATA SET
#cyStarts,cyFirsts,cySeconds,cyThirds,cyEps
#nWorkouts,AvgPos,Age, cyPlacePercentage
#############################

#removing career attributes
halving = analyze()
whole = halving.horseDataNoSale

#add additional column 'show ratio'
n,p = whole.shape
b = np.ones((n,1))
whole = np.concatenate((whole, b), axis=1) 
n,p = whole.shape
halfway = n/2



#calculating the show ratio as the last attribute
for i in range(0, n):
	totalShows = 0
	showRatio = 0
	for j in range(1,4):
		totalShows += whole[i][j]
	if(float(whole[i][0]) > 0):
		showRatio = float(totalShows)/float(whole[i][0])
	whole[i][8] = showRatio

half1, half2 = np.array_split(whole, [halfway])
nh1, p = half1.shape
nh2, p = half2.shape

positionsHalf1 = halving.positionsNoSale[:len(halving.positionsNoSale)/2]
positionsHalf2 = halving.positionsNoSale[len(halving.positionsNoSale)/2:]
positionsWhole = halving.positionsNoSale[:]

#perform PCA 
a,b,c = halving.PCA(half1, "corr")
print "BEGIN HALVED PCA"
print "First PC: \n%s\n" % a
print "Second PC: \n%s\n" % b
a = -1 * a
b = -1 * b
print "First PC flipped: \n%s\n" % a
print "Second PC flipped: \n%s\n" % b

ab = np.column_stack((a.flatten(), b.flatten()))
x = []
y = []

#project the data back onto the first two PCs:
normalizedHalf1 = halving.normalize(half1)
normalizedWhole = halving.normalize(whole)
for i in range(0, nh1):
	temp = np.dot(normalizedHalf1[i], ab)
	x.append(temp[0]) # PC 1
	y.append(temp[1]) # PC 2


#finally plotting the results from PCAs

cmap, norm = mpl.colors.from_levels_and_colors(levels=halving.levels, colors=halving.colors, extend='max')
plt.scatter(x,y,c=positionsHalf1, edgecolor='none', cmap=cmap, norm=norm)
xlabel = "PC 1 - 1sts, Show %"
ylabel = "PC 2 - nWorkouts, Workout Performance (position compared to others)"
title = "PCA First Half- nWorkouts, Workout Performance v. 1sts, Show %"
plt.xlabel(xlabel)
plt.ylabel(ylabel)
plt.title(title)
plt.show()



#################################
#projecting horses for each race  according the the above PCA
#################################
n,p = test.raceData.shape
i = halfway
totalRaces = 0
predictedAShow = 0
predicted2Shows = 0
predicted3Shows = 0

predictedAShownn = 0
predicted2Showsnn = 0
predicted3Showsnn = 0

cap = 0
while(i < 3270): #the amount of horses I have
#while(i < 3270):
	x2 = []
	y2 = []
	pos2 = []
	x2nn = []
	y2nn = []

	raceN = test.raceData[i][7]
	while(test.raceData[i][7] == raceN):
		if (test.raceData[i][0] in halving.namesNoSale):
			nameIndex = halving.namesNoSale.index(halving.raceData[i][0])
			tempRowN = normalizedWhole[nameIndex, :]
			tempRow = whole[nameIndex, :]
			pos2.append(halving.raceData[i][4])
			temp = np.dot(tempRowN, ab)
			x2.append(temp[0]) # PC 1
			y2.append(temp[1]) # PC 2
			tempnn = np.dot(tempRow, ab)
			x2nn.append(tempnn[0])
			y2nn.append(tempnn[1])
		i += 1
	totalRaces += 1
	tmp_showsInARace = 0
	tmp_predictedAShow = 0

	poslen = len(pos2)
	j = 0
	while( j < poslen and float(pos2[j]) < 4 ):
		greaterCount = 0
		for j2 in range(0,poslen):
			if (float(x2[j2]) > float(x2[j])):
				greaterCount += 1
		if (greaterCount < 3):
			tmp_showsInARace += 1
		j += 1

	#update the correct amount of shows in the race

	if(tmp_showsInARace > 0):
		predictedAShow += 1
		if(tmp_showsInARace > 1):
			predicted2Shows += 1
			if(tmp_showsInARace > 2):
				predicted3Shows += 1

	#measuring same stats but for a not normalized projection back on the PCs
	tmp_showsInARacenn = 0
	tmp_predictedAShownn = 0

	poslen = len(pos2)
	j = 0
	while( j < poslen and float(pos2[j]) < 4 ):
		greaterCount = 0
		for j2 in range(0,poslen):
			if (float(x2nn[j2]) > float(x2nn[j])):
				greaterCount += 1
		if (greaterCount < 3):
			tmp_showsInARacenn += 1
		j += 1

	#update the correct amount of shows in the race

	if(tmp_showsInARacenn > 0):
		predictedAShownn += 1
		if(tmp_showsInARacenn > 1):
			predicted2Showsnn += 1
			if(tmp_showsInARacenn > 2):
				predicted3Showsnn += 1

	if (cap < 6):
		cmap, norm = mpl.colors.from_levels_and_colors(levels=halving.levels, colors=halving.colors, extend='max')
		plt.scatter(x2,y2,c=pos2, edgecolor='none', cmap=cmap, norm=norm)
		xlabel = "PC 1 - 1sts, Show %"
		ylabel = "PC 2 - nWorkouts, Workout Performance (position compared to others)"
		title = "Half-PCA Race: " + str(raceN)	
		plt.xlabel(xlabel)
		plt.ylabel(ylabel)
		plt.title(title)
		plt.show()

		#not normalized projection
		plt.scatter(x2nn,y2nn,c=pos2, edgecolor='none', cmap=cmap, norm=norm)
		xlabel = "PC 1 - 1sts, Show %"
		ylabel = "PC 2 - nWorkouts, Workout Performance (position compared to others)"
		title = "Half-PCA, Non-normalized Projection - Race: " + str(raceN)	
		plt.xlabel(xlabel)
		plt.ylabel(ylabel)
		plt.title(title)
		plt.show()

		cap += 1

predictedAShowRatio = float(predictedAShow)/float(totalRaces)
predicted2ShowsRatio = float(predicted2Shows)/float(totalRaces)
predicted3ShowsRatio = float(predicted3Shows)/float(totalRaces)
print "predictedAShow Ratio: %f" % predictedAShowRatio
print "predicted2Shows Ratio: %f" % predicted2ShowsRatio
print "predicted3Shows Ratio: %f\n" % predicted3ShowsRatio

predictedAShowRationn = float(predictedAShownn)/float(totalRaces)
predicted2ShowsRationn = float(predicted2Showsnn)/float(totalRaces)
predicted3ShowsRationn = float(predicted3Showsnn)/float(totalRaces)
print "predictedAShownn Ratio: %f" % predictedAShowRationn
print "predicted2Showsnn Ratio: %f" % predicted2ShowsRationn
print "predicted3Showsnn Ratio: %f" % predicted3ShowsRationn




##################
##Plotting the show/firsts percentage for the above PCA
#################

x_shows = []
y_shows = []
y_losers = []
y_firsts = []
y_seconds = []
y_thirds = []

x_shows = np.linspace(-3, 5, 50)
xlen = len(x)
for div in x_shows:
	total = 0
	totalshows = 0
	totalfirsts = 0
	totallosers = 0
	totalseconds = 0
	totalthirds = 0
	for i in range(0, xlen):
		if(x[i] > div):
			total += 1
			if(float(positionsHalf1[i]) < 4):
				totalshows += 1
				if(float(positionsHalf1[i]) == 3):
					totalthirds += 1
				elif(float(positionsHalf1[i]) == 2):
					totalseconds += 1
				elif(float(positionsHalf1[i]) == 1):
					totalfirsts += 1
			else:
				totallosers += 1

	y_shows.append(float(totalshows)/float(total))
	y_firsts.append(float(totalfirsts)/float(total))
	y_seconds.append(float(totalseconds)/float(total))
	y_thirds.append(float(totalthirds)/float(total))
	y_losers.append(float(totallosers)/float(total))

plt.plot(x_shows,y_shows,c="green")
plt.plot(x_shows,y_firsts,c="yellow")
plt.plot(x_shows,y_seconds,c="silver")
plt.plot(x_shows,y_thirds,c="brown")
plt.plot(x_shows,y_losers,c="red")




xlabel = "PC 1 - 1sts, Show %"
ylabel = "Percentage of total horses laying in graph > xTick"
title = "PCA First Half - Percentage of Horses that Showed with PCA axes"
plt.xlabel(xlabel)
plt.ylabel(ylabel)
plt.title(title)
plt.show()


#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^]
#END OF HALVING THE DATA SET
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^]
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$



#############################
#CONTINUE BY REMOVING SOME ATTRIBUTES...MORE PCA
#cyStarts,cyFirsts,cySeconds,cyThirds,cyEps
#Price,nWorkouts,AvgPos,Age, cyPlacePercentage
#############################

#removing career attributes

masterData2 = np.delete(test.horseData, 5, 1)
for i in range(0,4):
	masterData2 = np.delete(masterData2, 5, 1)

#add additional column 'show ratio'
n,p = masterData2.shape
b = np.ones((n,1))
masterData2 = np.concatenate((masterData2, b), axis=1) 
n,p = masterData2.shape

#calculating the show ratio as the last attribute
for i in range(0, n):
	totalShows = 0
	showRatio = 0
	for j in range(1,4):
		totalShows += masterData2[i][j]
	if(float(masterData2[i][0]) > 0):
		showRatio = float(totalShows)/float(masterData2[i][0])
	masterData2[i][9] = showRatio

#perform PCA 
a,b,c = test.PCA(masterData2, "corr")
print "First PC: \n%s\n" % a
print "Second PC: \n%s\n" % b
a = -1 * a
b = -1 * b
print "First PC flipped: \n%s\n" % a
print "Second PC flipped: \n%s\n" % b
n, p = masterData2.shape
ab = np.column_stack((a.flatten(), b.flatten()))
x = []
y = []

#project the data back onto the first two PCs:
normalizedHorses = test.normalize(masterData2)
for i in range(0, n):
	temp = np.dot(normalizedHorses[i], ab)
	x.append(temp[0]) # PC 1
	y.append(temp[1]) # PC 2

positions2 = test.positions[:]


#finally plotting the results from PCAs

cmap, norm = mpl.colors.from_levels_and_colors(levels=test.levels, colors=test.colors, extend='max')
plt.scatter(x,y,c=positions2, edgecolor='none', cmap=cmap, norm=norm)
xlabel = "PC 1 - 1sts, Show %"
ylabel = "PC 2 - nWorkouts, Workout Performance"
title = "PCA 2 - nWorkouts, Workout Performance v. 1sts, Show %"
plt.xlabel(xlabel)
plt.ylabel(ylabel)
plt.title(title)
plt.show()



#################################
#projecting horses for each race  according the the above PCA
#################################
n,p = test.raceData.shape
i = 0
totalRaces = 0
predictedAShow = 0
predicted2Shows = 0
predicted3Shows = 0

cap = 0
#while(i < 3270 and cap < 4): #the amount of horses I have
while(i < 3270):
	x2 = []
	y2 = []
	pos2 = []
	raceN = test.raceData[i][7]
	while(test.raceData[i][7] == raceN):
		if (test.raceData[i][0] in test.names):
			nameIndex = test.names.index(test.raceData[i][0])
			tempRowN = normalizedHorses[nameIndex, :]
			tempRow = masterData2[nameIndex, :]
			pos2.append(test.raceData[i][4])
			temp = np.dot(tempRowN, ab)
			x2.append(temp[0]) # PC 1
			y2.append(temp[1]) # PC 2
		i += 1

	totalRaces += 1
	sortedx2 = x2[:]
	sortedx2.sort()

	tmp_showsInARace = 0

	poslen = len(pos2)
	j = 0
	while( j < poslen and float(pos2[j]) < 4 ):
		greaterCount = 0
		for j2 in range(0,poslen):
			if (float(x2[j2]) > float(x2[j])):
				greaterCount += 1
		if (greaterCount < 3):
			tmp_showsInARace += 1
		j += 1

	#update the correct amount of shows in the race

	if(tmp_showsInARace > 0):
		predictedAShow += 1
		if(tmp_showsInARace > 1):
			predicted2Shows += 1
			if(tmp_showsInARace > 2):
				predicted3Shows += 1

	if (cap < 6):
		cmap, norm = mpl.colors.from_levels_and_colors(levels=test.levels, colors=test.colors, extend='max')
		plt.scatter(x2,y2,c=pos2, edgecolor='none', cmap=cmap, norm=norm)
		xlabel = "PC 1 - 1sts, Show %"
		ylabel = "PC 2 - nWorkouts, Workout Performance (position compared to others)"
		title = "PCA with Sale Price - Race: " + str(raceN)	
		plt.xlabel(xlabel)
		plt.ylabel(ylabel)
		plt.title(title)
		plt.show()
		cap += 1

predictedAShowRatio = float(predictedAShow)/float(totalRaces)
predicted2ShowsRatio = float(predicted2Shows)/float(totalRaces)
predicted3ShowsRatio = float(predicted3Shows)/float(totalRaces)
print "predictedAShow Ratio: %f" % predictedAShowRatio
print "predicted2Shows Ratio: %f" % predicted2ShowsRatio
print "predicted3Shows Ratio: %f" % predicted3ShowsRatio





##################
##Plotting the show/firsts percentage for the above PCA
#################

x_shows = []
y_shows = []
y_losers = []
y_firsts = []
y_seconds = []
y_thirds = []

x_shows = np.linspace(-3, 5, 50)
xlen = len(x)
for div in x_shows:
	total = 0
	totalshows = 0
	totalfirsts = 0
	totallosers = 0
	totalseconds = 0
	totalthirds = 0
	for i in range(0, xlen):
		if(x[i] > div):
			total += 1
			if(float(positions2[i]) < 4):
				totalshows += 1
				if(float(positions2[i]) == 3):
					totalthirds += 1
				elif(float(positions2[i]) == 2):
					totalseconds += 1
				elif(float(positions2[i]) == 1):
					totalfirsts += 1
			else:
				totallosers += 1

	y_shows.append(float(totalshows)/float(total))
	y_firsts.append(float(totalfirsts)/float(total))
	y_seconds.append(float(totalseconds)/float(total))
	y_thirds.append(float(totalthirds)/float(total))
	y_losers.append(float(totallosers)/float(total))

plt.plot(x_shows,y_shows,c="green")
plt.plot(x_shows,y_firsts,c="yellow")
plt.plot(x_shows,y_seconds,c="silver")
plt.plot(x_shows,y_thirds,c="brown")
plt.plot(x_shows,y_losers,c="red")




xlabel = "PC 1 - 1sts, Show %"
ylabel = "Percentage of total horses laying in graph > xTick"
title = "PCA 2 - Percentage of Horses that Showed with PC 1"
plt.xlabel(xlabel)
plt.ylabel(ylabel)
plt.title(title)
plt.show()

#######################################################
##Plot the bar graph with percentages past 0.5 on PC 1
#######################################################
y = [y_losers[21], y_shows[21], y_firsts[21], y_seconds[21], y_thirds[21]]
x = scipy.arange(5)
#f = plt.figure()
#ax = f.add_axes([0.1, 0.1, 0.8, 0.8])
plt.bar(x, y, align='center')
#ax.set_xticks(x)
#ax.set_xticklabels(['Losers', 'Shows', 'Firsts', 'Seconds', 'Thirds'])
#ylabel = "Percentage of Horses With Projection on PC 1 > 0.5"
title = "PCA 2 - Horse Performance Relative to PC 1"

#f.ylabel(ylabel)
plt.title(title)

plt.show()

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@

###################
#DANGER ZONE
###################
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@

#############################
#CONTINUE BY REMOVING SOME ATTRIBUTES...MORE PCA
#cyStarts,cyFirsts,cySeconds,cyThirds,cyEps
#nWorkouts,AvgPos,Age, cyPlacePercentage
#############################

#removing career attributes

masterData2NoSale = test.horseDataNoSale

#add additional column 'show ratio'
n,p = masterData2NoSale.shape
b = np.ones((n,1))
masterData2NoSale = np.concatenate((masterData2NoSale, b), axis=1) 
n,p = masterData2NoSale.shape

#calculating the show ratio as the last attribute
for i in range(0, n):
	totalShows = 0
	showRatio = 0
	for j in range(1,4):
		totalShows += masterData2NoSale[i][j]
	if(float(masterData2NoSale[i][0]) > 0):
		showRatio = float(totalShows)/float(masterData2NoSale[i][0])
	masterData2NoSale[i][8] = showRatio

#perform PCA 
a,b,c = test.PCA(masterData2NoSale, "corr")
print "BEGIN NO SALE"
print "First PC: \n%s\n" % a
print "Second PC: \n%s\n" % b
a = -1 * a
b = -1 * b
print "First PC flipped: \n%s\n" % a
print "Second PC flipped: \n%s\n" % b
n, p = masterData2NoSale.shape
ab = np.column_stack((a.flatten(), b.flatten()))
x = []
y = []

#project the data back onto the first two PCs:
normalizedHorsesNoSale = test.normalize(masterData2NoSale)
for i in range(0, n):
	temp = np.dot(normalizedHorsesNoSale[i], ab)
	x.append(temp[0]) # PC 1
	y.append(temp[1]) # PC 2

positions2NoSale = test.positionsNoSale[:]


#finally plotting the results from PCAs

cmap, norm = mpl.colors.from_levels_and_colors(levels=test.levels, colors=test.colors, extend='max')
plt.scatter(x,y,c=positions2NoSale, edgecolor='none', cmap=cmap, norm=norm)
xlabel = "PC 1 - 1sts, Show %"
ylabel = "PC 2 - nWorkouts, Workout Performance (position compared to others)"
title = "PCA No Sale - nWorkouts, Workout Performance v. 1sts, Show %"
plt.xlabel(xlabel)
plt.ylabel(ylabel)
plt.title(title)
plt.show()



#################################
#projecting horses for each race  according the the above PCA
#################################
n,p = test.raceData.shape
i = 0
totalRaces = 0
predictedAShow = 0
predicted2Shows = 0
predicted3Shows = 0

cap = 0
#while(i < 3270 and cap < 4): #the amount of horses I have
while(i < 3270):
	x2 = []
	y2 = []
	pos2 = []
	raceN = test.raceData[i][7]
	while(test.raceData[i][7] == raceN):
		if (test.raceData[i][0] in test.namesNoSale):
			nameIndex = test.namesNoSale.index(test.raceData[i][0])
			tempRowN = normalizedHorsesNoSale[nameIndex, :]
			tempRow = masterData2NoSale[nameIndex, :]
			pos2.append(test.raceData[i][4])
			temp = np.dot(tempRowN, ab)
			x2.append(temp[0]) # PC 1
			y2.append(temp[1]) # PC 2
		i += 1
	totalRaces += 1
	tmp_showsInARace = 0
	tmp_predictedAShow = 0

	poslen = len(pos2)
	j = 0
	while( j < poslen and float(pos2[j]) < 4 ):
		greaterCount = 0
		for j2 in range(0,poslen):
			if (float(x2[j2]) > float(x2[j])):
				greaterCount += 1
		if (greaterCount < 3):
			tmp_showsInARace += 1
		j += 1

	#update the correct amount of shows in the race

	if(tmp_showsInARace > 0):
		predictedAShow += 1
		if(tmp_showsInARace > 1):
			predicted2Shows += 1
			if(tmp_showsInARace > 2):
				predicted3Shows += 1
	if(cap < 6):
		cmap, norm = mpl.colors.from_levels_and_colors(levels=test.levels, colors=test.colors, extend='max')
		plt.scatter(x2,y2,c=pos2, edgecolor='none', cmap=cmap, norm=norm)
		xlabel = "PC 1 - 1sts, Show %"
		ylabel = "PC 2 - nWorkouts, Workout Performance (position compared to others)"
		title = "PCA - Without Sale Price, Full DataSet - Race: " + str(raceN)	
		plt.xlabel(xlabel)
		plt.ylabel(ylabel)
		plt.title(title)
		plt.show()
		cap += 1

predictedAShowRatio = float(predictedAShow)/float(totalRaces)
predicted2ShowsRatio = float(predicted2Shows)/float(totalRaces)
predicted3ShowsRatio = float(predicted3Shows)/float(totalRaces)
print "predictedAShow Ratio: %f" % predictedAShowRatio
print "predicted2Shows Ratio: %f" % predicted2ShowsRatio
print "predicted3Shows Ratio: %f" % predicted3ShowsRatio





##################
##Plotting the show/firsts percentage for the above PCA
#################

x_shows = []
y_shows = []
y_losers = []
y_firsts = []
y_seconds = []
y_thirds = []

x_shows = np.linspace(-3, 5, 50)
xlen = len(x)
for div in x_shows:
	total = 0
	totalshows = 0
	totalfirsts = 0
	totallosers = 0
	totalseconds = 0
	totalthirds = 0
	for i in range(0, xlen):
		if(x[i] > div):
			total += 1
			if(float(positions2NoSale[i]) < 4):
				totalshows += 1
				if(float(positions2NoSale[i]) == 3):
					totalthirds += 1
				elif(float(positions2NoSale[i]) == 2):
					totalseconds += 1
				elif(float(positions2NoSale[i]) == 1):
					totalfirsts += 1
			else:
				totallosers += 1

	y_shows.append(float(totalshows)/float(total))
	y_firsts.append(float(totalfirsts)/float(total))
	y_seconds.append(float(totalseconds)/float(total))
	y_thirds.append(float(totalthirds)/float(total))
	y_losers.append(float(totallosers)/float(total))

plt.plot(x_shows,y_shows,c="green")
plt.plot(x_shows,y_firsts,c="yellow")
plt.plot(x_shows,y_seconds,c="silver")
plt.plot(x_shows,y_thirds,c="brown")
plt.plot(x_shows,y_losers,c="red")




xlabel = "PC 1 - 1sts, Show %"
ylabel = "Percentage of total horses laying in graph > xTick"
title = "PCA No Sale - Percentage of Horses that Showed with PCA axes"
plt.xlabel(xlabel)
plt.ylabel(ylabel)
plt.title(title)
plt.show()

#######################################################
##Plot the bar graph with percentages past 0.5 on PC 1
#######################################################
y = [y_losers[21], y_shows[21], y_firsts[21], y_seconds[21], y_thirds[21]]
x = scipy.arange(5)
#f = plt.figure()
#ax = f.add_axes([0.1, 0.1, 0.8, 0.8])
plt.bar(x, y, align='center')
#ax.set_xticks(x)
#ax.set_xticklabels(['Losers', 'Shows', 'Firsts', 'Seconds', 'Thirds'])
ylabel = "Percentage of Horses With Projection on PC 1 > 0.5"
title = "PCA No Sale - Horse Performance Relative to PC 1"

plt.title(title)

plt.show()

##############
###############
###############
#END DANGER ZONE
#############################
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@



#########################################
###PCA MASTER 2b - Plot every attribute###
#########################################
labels = [	"Starts", "1sts", "2nds", "3rds", "EPS", 
			"Auction Price", "nWorkouts", 
			"Workout Position", "Age", "Show %"		]

fig = plt.figure(figsize=(15,15))
X = masterData2
n,p = np.shape(X)
for i in range(0, p):
	for j in range(0, p):
		k = (j + 1) + (p * i)
		plt.subplot(p, p, k)
		plt.scatter(X[:,j],X[:,i],c=test.positions, edgecolor='none', cmap=cmap, norm=norm)

		plt.axis([np.amin(X[:,j]) - 1, np.amax(X[:,j]) + 1, np.amin(X[:,i]) - 1, np.amax(X[:,i]) + 1])
		frame = plt.gca()
		frame.axes.get_xaxis().set_ticks([])
		frame.axes.get_yaxis().set_ticks([])
		xlabel = labels[j]
		ylabel = labels[i]

		plt.xlabel(xlabel)
		plt.ylabel(ylabel)
fig.tight_layout()
plt.show()

#############################
#CONTINUE BY REMOVING SOME ATTRIBUTES...MORE PCA
#cyEPS, auction price, age, cyShow %
#############################

n,p = masterData2.shape
masterData3 = masterData2[:,:]
masterData3 = np.delete(masterData3, 0, 1)
masterData3 = np.delete(masterData3, 0, 1)
masterData3 = np.delete(masterData3, 0, 1)
masterData3 = np.delete(masterData3, 0, 1)
masterData3 = np.delete(masterData3, 2, 1)
masterData3 = np.delete(masterData3, 2, 1)

n,p = masterData3.shape

a,b,c = test.PCA(masterData3, "corr")
print "First PC: \n%s\n" % a
print "Second PC: \n%s\n" % b

a = -1 * a
b = -1 * b

print "First PC flipped: \n%s\n" % a
print "Second PC flipped: \n%s\n" % b

ab = np.column_stack((a.flatten(), b.flatten()))
x = []
y = []

#project the data back onto the first two PCs:
normalizedHorses3 = test.normalize(masterData3)
for i in range(0, n):
	temp = np.dot(normalizedHorses3[i], ab)
	x.append(temp[0]) # PC 1
	y.append(temp[1]) # PC 2

positions = test.positions[:]


#finally plotting the results from PCAs

cmap, norm = mpl.colors.from_levels_and_colors(levels=test.levels, colors=test.colors, extend='max')

plt.scatter(x,y,c=positions, edgecolor='none', cmap=cmap, norm=norm)
xlabel = "PC 1 - EPS, Show %"
ylabel = "PC 2 - Age, Auction Price"
title = "PCA 3 - Age, Auction Price v. EPS, Show %"
plt.xlabel(xlabel)
plt.ylabel(ylabel)
plt.title(title)
plt.show()


####################################################
#####PLOTTING JUST 4 attributes from above against each other
####################################################

labels = [	"EPS", "Auction Price", "Age", "Show %"]

fig = plt.figure(figsize=(15,15))
X = masterData3
n,p = np.shape(X)
for i in range(0, p):
	for j in range(0, p):
		k = (j + 1) + (p * i)
		plt.subplot(p, p, k)
		plt.scatter(X[:,j],X[:,i],c=test.positions, edgecolor='none', cmap=cmap, norm=norm)

		plt.axis([np.amin(X[:,j]) - 1, np.amax(X[:,j]) + 1, np.amin(X[:,i]) - 1, np.amax(X[:,i]) + 1])
		frame = plt.gca()
		frame.axes.get_xaxis().set_ticks([])
		frame.axes.get_yaxis().set_ticks([])
		xlabel = labels[j]
		ylabel = labels[i]

		plt.xlabel(xlabel)
		plt.ylabel(ylabel)
fig.tight_layout()
plt.show()



