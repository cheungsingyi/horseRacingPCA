import urllib2
import urllib
import random
import json

class proxyRequest:

	proxyList = [
					{"http": "107.167.111.29:80"},
					{"http": "185.26.183.64:443"},
					{"http": "62.23.15.92:3128"},
					{"http": "195.4.135.35:8080"},
					{"http": "197.254.46.150:3128"},
					{"http": "186.219.0.136:8080"},
					{"http": "59.106.218.227:3128"},
					{"http": "93.127.116.198:3128"},
					{"http": "54.209.77.153:3128"},
					{"http": "59.106.216.155:3128"},
					{"http": "150.107.80.203:80"},
					{"http": "107.151.136.203:80"},
					{"http": "104.250.147.22:81"},
					{"http": "5.196.190.108:4444"},
					{"http": "108.59.10.141:55555"},
					{"http": "151.1.216.181:80"},
					{"http": "178.82.166.148:80"},
					{"http": "104.236.220.70:80"}

					]
	proxyListOld = [
					{"http": "216.251.125.102:80"},
					{"http": "104.209.182.251:3128"},
					{"http": "173.220.170.242:7004"},
					#{"http": "151.1.216.181:80"},
					{"http": "192.99.44.195:3128"},
					{"http": "192.99.54.110:80"},
					{"http": "51.254.103.206:3128"},
					{"http": "46.101.92.7:3128"},
					{"http": "195.3.113.170:8000"},
					{"http": "176.9.59.80:3128"},
					{"http": "92.109.93.49:80"},
					{"http": "107.167.111.44:80"},
					{"http": "47.88.104.164:3128"},
					#{"http": "54.201.49.114:80"}, 
					{"http": "68.87.73.163:80"}, 
					{"http": "107.167.111.29:80"}, 
					{"http": "85.114.130.226:3128"}, 
					#{"http": "158.69.206.63:80"}, 
					#{"http": "107.151.136.205:80"}, 
					{"http": "158.69.206.63:8080"}, 
					{"http":"http://146.20.68.224:3128"}, 
					#{"http":"http://104.250.146.37:81"}, 
					#{"http":"http://107.151.152.218:80"}, 
					#{"http":"http://107.151.152.210:80"}, 
					#{"http":"http://108.61.158.182:8080"},

					{"http":"107.151.142.117:80"},
					{"http":"107.151.142.115:80"},
					{"http":"107.151.142.126:80"},
					{"http":"80.57.110.15:80"},
					{"http":"86.14.249.58:80"},
					{"http":"50.240.46.244:7004"},
					{"http":"213.136.79.122:80"},
					{"http":"109.207.61.139:8090"},
					{"http":"77.58.86.128:80"},
					{"http":"54.167.212.197:80"},
					{"http":"46.231.117.154:80"},
					{"http":"81.30.69.3:80"},
					{"http":"107.151.142.124:80"},
					{"http":"107.151.136.197:80"},
					{"http":"107.151.136.213:80"},
					{"http":"107.151.142.125:80"},
					{"http":"107.151.136.202:80"}
				]

	responseAcquired = 0
	proxyFailures = {}
	proxyAttempts = {}


	def __init__(self):
		for proxy in self.proxyList:
			self.proxyFailures[proxy['http']] = 0
			self.proxyAttempts[proxy['http']] = 0


	def getRequest(self, url):
		self.responseAcquired = 0
		html = ""
		while (not self.responseAcquired):
			proxy = random.choice(self.proxyList)
			proxies = urllib2.ProxyHandler(proxy)
			print "using proxy: %s" % proxy['http']
			self.proxyAttempts[proxy['http']] += 1 

			request = urllib2.Request(url)
			request.add_header("User-Agent", "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:25.0) Gecko/20100101 Firefox/25.0")
			request.add_header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")

			opener = urllib2.build_opener(proxies)
			urllib2.install_opener(opener)
			html = ""

			try:
				r = urllib2.urlopen(request, timeout=10)
				html = r.read()
				break
			except:
				print "WARNING: COULD NOT CONNECT WITH PROXY: %s" % proxy
				self.proxyFailures[proxy['http']] += 1 
				self.outputProxyAttempts()
				continue
			self.outputProxyAttempts()
			
		return html

	def postRequest(self, url, params):
		self.responseAcquired = 0
		html = ""
		while (not self.responseAcquired):
			proxy = random.choice(self.proxyList)
			proxies = urllib2.ProxyHandler(proxy)
			print "using proxy: %s" % proxy['http']
			self.proxyAttempts[proxy['http']] += 1 

			request = urllib2.Request(url)
			request.add_header("User-Agent", "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:25.0) Gecko/20100101 Firefox/25.0")
			request.add_header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")

			opener = urllib2.build_opener(proxies)
			urllib2.install_opener(opener)

			try:
				r = urllib2.urlopen(request, urllib.urlencode(params), timeout=10)
				html = r.read()
				return html
			except:
				print "WARNING: COULD NOT CONNECT WITH PROXY: %s" % proxy
				self.proxyFailures[proxy['http']] += 1 
				continue
			self.outputProxyAttempts()

	def outputProxyAttempts(self):
		with open('proxyAttempts.txt', 'w+') as outfile:
			json.dump(self.proxyAttempts, outfile, indent=4, separators=(',',': '))
			json.dump(self.proxyFailures, outfile, indent=4, separators=(',',': '))
		

	def generateProxyList(self):
		proxyList = []
		r = urllib2.urlopen("https://incloak.com/proxy-list/?country=US&type=h")
		html = r.read()
		f = open("proxyListTest.html", 'w+')
		f.write(html)
		f.close()
		self.proxyList = proxyList

pltest = proxyRequest()
pltest.generateProxyList()
