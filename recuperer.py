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
	
	def processXMLtag(self, champs):
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
	
	def processXMLid(self, champs):
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
			with open(f"{code}.csv", "r") as f:
				self.data[code] = f.read()
				f.close()
	
	def getAll(self):
		self.dataparsed = {}
		for code in self.name:	
			self.data[code] = self.data[code].split("\n")
			for index, val in enumerate(self.data[code]):
				self.data[code][index] = val.split(";")
			
			self.dataparsed[code] = {}
			for index, field in enumerate(self.data[code][0]):
				self.dataparsed[code][field] =  []
				for line in range(1, len(self.data[code])-1):
					self.dataparsed[code][field].append(self.data[code][line][index])
		
	def returnData(self):
		return self.dataparsed

if __name__ == "__main__":
	endpoints = {'FR_MTP_ANTI': 'Antigone', 'FR_MTP_COME': 'Comédie', 'FR_MTP_CORU': 'Corum', 'FR_MTP_EURO': 'Europa', 'FR_MTP_FOCH': 'Foch', 'FR_MTP_GAMB':     'Gambetta', 'FR_MTP_GARE': 'Gare', 'FR_MTP_TRIA': 'Triangle', 'FR_MTP_ARCT': 'Arc de Triomphe', 'FR_MTP_PITO': 'Pitot', 'FR_MTP_CIRC': 'Circe', 'FR_MTP_S    ABI': 'Sabines', 'FR_MTP_GARC': 'Garcia Lorca', 'FR_MTP_SABL': 'Sablassou', 'FR_MTP_MOSS': 'Mosson', 'FR_STJ_SJLC': 'Saint Jean le Sec', 'FR_MTP_MEDC': '    Euromédecine', 'FR_MTP_OCCI': 'Occitanie', 'FR_CAS_VICA': 'Vicarello', 'FR_MTP_GA109': 'Gaumont EST', 'FR_MTP_GA250': 'Gaumont OUEST', 'FR_CAS_CDGA': 'Ch    arles de Gaulle', 'FR_MTP_ARCE': 'Arceaux', 'FR_MTP_POLY': 'Polygone'}
	champs = {"DateTime": "Heure d'actualisation", "Name": "Nom du parking", "Status": "Status", "Free": "Place(s) libre(s)", "Total": "Nombre de places"}
