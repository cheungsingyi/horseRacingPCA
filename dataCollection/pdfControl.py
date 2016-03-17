from equibasepdfScraper import equibasePdfScraper
from pdfhandling import pdfHandler
import os

class pdfControl:
	csvOutFile= "/Users/markusnotti/Documents/UCLA/Winter2016/170A-Mathmatical Modeling and Methods for Computer Science/horseRacing/data/decryptedResultsData/resultsCSV/raceResults.csv"
	decryptedPath="/Users/markusnotti/Documents/UCLA/Winter2016/170A-Mathmatical Modeling and Methods for Computer Science/horseRacing/data/decryptedResultsData"

	def __init__(self):
		##decrypts all pdfs and places them in usable dir
		pdfHandler()

		##grab all decrypted pdfs
		decryptedPdfs = self.getDecryptedPdfs()

		##grabs info from pdfs and places race results in csv
		scraper = equibasePdfScraper()
		scraper.parse(decryptedPdfs, self.csvOutFile)

	def getDecryptedPdfs(self):
		dirfiles = os.listdir(self.decryptedPath)
		decryptedPdfs = []
		for f in dirfiles:
			if( f[len(f)-4:] == ".pdf"):
				decryptedPdfs.append(self.decryptedPath + "/" + f)
		return decryptedPdfs

pdfControl()




