# Elouan FIORE
# Version 0.5

from lxml import etree
import requests
import time

class API():
	def __init__(self, url, log=1):
		self.url = url
		self.loglevel = log
	
	def downloadEndpoints(self, endpoints):
		error = 0
		self.endpointsData = {}
		for code in endpoints:
			if self.loglevel >= 2:
				self.log(f"Downloading {code}...")
			
			reponse = requests.get(self.url.format(code))
			status = reponse.status_code

			if status == 200:
				self.endpointsData[code] = reponse.content
			else:
				error += 1
				if self.loglevel >=2:
					self.log(f"Error {status}")
		
		if self.loglevel >= 1:
			self.log(f"########## End downloading, {error} error(s) ##########\n")
	
	def processXML(self, champs):
		self.endpointsParse = {}
		for code, contenu in self.endpointsData.items():
			if self.loglevel >= 2:
				self.log(f"Converting {code}...")
			contenu = etree.fromstring(contenu)	
			
			if self.loglevel >= 2:
				self.log(f"Processing {code}...")
			self.endpointsParse[code] = {}
			
			for champ in champs:
				for i in contenu:
					if i.tag == champ:
						self.endpointsParse[code][champ] = i.text
		
		if self.loglevel >= 1:
			self.log(f"End processing\n")
	
	def saveCSV(self, chemin="."):
		for code, contenu in self.endpointsParse.items():
			if self.loglevel >= 2:
				sel.loglevel(f"Sauving {code}...")
			
			line = ""
			for champs, data in contenu.items():
				line += f"{data};"
			
			try:
				fichier = open(f"{chemin}/{code}.csv", "r")
				fichier.close()
			except FileNotFoundError:
				header = ";".join(contenu.keys())
				with open(f"{chemin}/{code}.csv", "w") as fichier:
					fichier.write(f"{header}\n{line}\n")
					fichier.close()
			else:
				with  open(f"{chemin}/{code}.csv", "a") as fichier:
					fichier.write(f"{line}\n")
					fichier.close()
		if self.loglevel >= 1:
			self.log("End saving\n")
	
	def print(self):
		for code, contenu in self.endpointsParse.items():
			print(f"\n{code}")
			for champ, data in contenu.items():
				print(f"	{champ} : {data}")

	def runFor(self, lenght, sleep, function):
		endTime = int(time.time()) + lenght*60
		execute = 0
		sleep *= 60

		while int(time.time()) < endTime:
			execTime = int(time.time())
			function()
			execTime = int(time.time()) - execTime
			execute += 1
			time.sleep(sleep - execTime)
		
		if self.loglevel >= 1:
			self.log(f"Exécuté {execute} fois")
	
	def log(self, message):
		print(message)
		with open("recup.log", "a") as f:
			f.write(message)
			f.close()

class CSV():
	def __init__(self, name, path="."):
		self.name = name
		self.data = {}
		for code in self.name:
			with open("", "r") as f:
				self.data[code] = f.read()
				f.close()
			
			self.data[code] = self.data[code].split("\n")
			for index, val in enumerate(self.data[code]):
				self.data[code][index] = val.split("\n")
			self.data[code] = self.data[code][1:-1]
	
	def getAll(fields):
		self.dataparsed = {}
		for code in self.name:
			self.dataparsed[code] = {}
			for index in fields:
				self

if __name__ == "__main__":
	url = "https://data.montpellier3m.fr/sites/default/files/ressources/{}.xml"
	url_list = ["FR_MTP_ANTI", "FR_MTP_COME", "FR_MTP_CORU", "FR_MTP_EURO", "FR_MTP_FOCH", "FR_MTP_GAMB", "FR_MTP_GARE", "FR_MTP_TRIA", "FR_MTP_ARCT", "FR_MTP_PITO", "FR_MTP_CIRC", "FR_MTP_SABI", "FR_MTP_GARC", "FR_MTP_SABL", "FR_MTP_MOSS", "FR_STJ_SJLC", "FR_MTP_MEDC", "FR_MTP_OCCI", "FR_CAS_VICA", "FR_MTP_GA109", "FR_MTP_GA250", "FR_CAS_CDGA", "FR_MTP_ARCE", 'FR_MTP_POLY']
	champs = ["DateTime", "Name", "Status", "Free", "Total"]
	park = API(url)
	
	def test():	
		park.downloadEndpoints(url_list)
		park.processXML(champs)
		park.saveCSV()

	park.runFor(1, 0.5, test)
