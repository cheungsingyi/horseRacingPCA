import os
import sys
from subprocess import call

class pdfHandler:
	#either path works... the first is absolute and would work wherever this class is stored so it is preferred in this case
	path = "/Users/markusnotti/Documents/UCLA/Winter2016/170A-Mathmatical Modeling and Methods for Computer Science/horseRacing/data"
	path2 = "../data"

	def __init__(self):
		self.findPdfsInDir(self.path)

	def findPdfsInDir(self, dirPath):
		pdfs = []
		dirfiles = os.listdir(dirPath)
		self.decrypt(dirfiles, dirPath)
	
	def decrypt(self, dirfiles, dirPath):
		for f in dirfiles:
			if( f[len(f)-4:] == ".pdf"):
				if(not os.path.isfile(dirPath + "/decryptedResultsData/decrypted-" + f )):
					call(["qpdf", "--decrypt", dirPath + "/" + f, dirPath + "/decryptedResultsData/decrypted-" + f])
					print "created decrypted-" + f
				else:
					print "decrypted-" + f + " already exists..."



pdfHandler()

