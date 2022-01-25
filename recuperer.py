# -*- coding: utf-8 -*-
# Elouan FIORE Léo BRUALLA
# Version 1


from lxml import etree
import requests
import time

class API():
	def __init__(self, url, log=1):
		self.url = url
		self.loglevel = log
	
	def downloadEndpoints(self, lst=[]):
		error = 0
		self.endpointsData = {}

		for code in lst:
			self.log(2, f"Downloading {code}...")

			reponse = requests.get(self.url.format(code))
			status = reponse.status_code

			if status == 200:
				self.endpointsData[code] = reponse.content
			else:
				error += 1
				self.log(0, f"ERROR {code} {status}")
		
		self.log(1, f"################################# End downloading, {error} error(s) #################################")
	

	def processXML(self, field, id=[], timecap=0):
		self.endpointsParse = {}
		if timecap == 0:
			now = time.localtime(time.time())
			timecap = time.strftime("%d/%m/%Y-%H:%M", now)

		if id == []:
			for code, contenu in self.endpointsData.items():
				self.log(2, f"Converting {code}...")
				contenu = etree.fromstring(contenu)	

				self.log(2, f"Processing {code}...")
				self.endpointsParse[code] = {}

				self.endpointsParse[code]["CapTime"] = timecap
				for f in field:
					for i in contenu:
						if i.tag == f:
							self.endpointsParse[code][f] = i.text
		else:
			for code, contenu in self.endpointsData.items():
				self.log(2, f"Converting {code}...")
				contenu = etree.fromstring(contenu)
				contenu = list(contenu)[0]

				for i in id:
					self.log(2, f"Processing {i}...")
					self.endpointsParse[i] = {}

					self.endpointsParse[i]["CapTime"] = timecap
					for element in contenu:
						attr = element.attrib
						
						if attr["id"] == i:
							for f in field:
								self.endpointsParse[i][f] = attr[f]

		self.log(1, f"####################################### End processing ########################################")

	def saveCSV(self, path="."):
		for code, contenu in self.endpointsParse.items():
			self.log(2, f"Saving {code}...")
			
			line = ""
			for data in contenu.values():
				line += f"{data};"
			
			try:
				fichier = open(f"{path}/{code}.csv", "r")
				fichier.close()
			except FileNotFoundError:
				header = ";".join(contenu.keys())
				with open(f"{path}/{code}.csv", "w") as fichier:
					fichier.write(f"{header}\n{line}\n")
					fichier.close()
			else:
				with  open(f"{path}/{code}.csv", "a") as fichier:
					fichier.write(f"{line}\n")
					fichier.close()
		
		self.log(1, "######################################### End saving ##########################################")
	
	def print(self):
		for code, contenu in self.endpointsParse.items():
			print(f"{code}")
			for field, data in contenu.items():
				print(f"	{field} : {data}")

	def runFor(self, lenght, sleep, function):
		endTime = int(time.time()) + lenght*60
		execute = 0
		sleep *= 60

		while int(time.time()) < endTime:
			execTime = int(time.time())
			function()
			execTime = int(time.time()) - execTime
			execute += 1
			self.log(1, f"##################################### Sleeping for {sleep/60} min #####################################")
			time.sleep(sleep - execTime)
		
		self.log(1, f"Executed {execute} time(s)")
	
	def log(self, level, message):
		now = time.localtime(time.time())
		message = time.strftime("%d/%m/%Y %H:%M ; ", now) + message
		if self.loglevel >= level:
			print(message)
			with open("recup.log", "a") as f:
				f.write(f"{message}\n")
				f.close()

class CSV():
	def __init__(self, name, path="."):
		self.name = name
		self.data = {}
		self.dataparsed = {}
	
		for code in self.name:
			with open(f"{path}/{code}.csv", "r") as f:
				self.data[code] = f.read()
				f.close()
	
	def getOne(self, code):
		if code in self.dataparsed.keys():
			return self.dataparsed[code]
		
		else:
			parsed = {}
			
			self.data[code] = self.data[code].split("\n")
			for index, val in enumerate(self.data[code]):
				self.data[code][index] = val.split(";")
			
			for index, field in enumerate(self.data[code][0]):
				parsed[field] = []	
				
				for line in range(1, len(self.data[code])-1):
					parsed[field].append(self.data[code][line][index])

			self.dataparsed[code] = parsed
			return parsed
	
	def getFromList(self, list):
		listparsed = {}
		
		for code in list:
			if code in self.dataparsed.keys():
				listparsed[code] = self.dataparsed[code]
			
			else:
				listparsed[code] = {}
				
				self.data[code] = self.data[code].split("\n")
				for index, val in enumerate(self.data[code]):
					self.data[code][index] = val.split(";")

				for index, field in enumerate(self.data[code][0]):
					listparsed[code][field] =  []
					
					for line in range(1, len(self.data[code])-1):
						listparsed[code][field].append(self.data[code][line][index])

				self.dataparsed[code] = listparsed[code]

		return listparsed

if __name__ == "__main__":
	url = "https://data.montpellier3m.fr/sites/default/files/ressources/{}.xml"
	
	endpointsvoi = {'FR_MTP_ANTI': 'Antigone', 'FR_MTP_COME': 'Comédie', 'FR_MTP_CORU': 'Corum', 'FR_MTP_EURO': 'Europa', 'FR_MTP_FOCH': 'Foch', 'FR_MTP_GAMB': 'Gambetta', 'FR_MTP_GARE': 'Gare', 'FR_MTP_TRIA': 'Triangle', 'FR_MTP_ARCT': 'Arc de Triomphe', 'FR_MTP_PITO': 'Pitot', 'FR_MTP_CIRC': 'Circe', 'FR_MTP_SABI': 'Sabines', 'FR_MTP_GARC': 'Garcia Lorca', 'FR_MTP_SABL': 'Sablassou', 'FR_MTP_MOSS': 'Mosson', 'FR_STJ_SJLC': 'Saint Jean le Sec', 'FR_MTP_MEDC': '    Euromédecine', 'FR_MTP_OCCI': 'Occitanie', 'FR_CAS_VICA': 'Vicarello', 'FR_MTP_GA109': 'Gaumont EST', 'FR_MTP_GA250': 'Gaumont OUEST', 'FR_CAS_CDGA': 'Charles de Gaulle', 'FR_MTP_ARCE': 'Arceaux', 'FR_MTP_POLY': 'Polygone'}
	champsvoi = {"DateTime": "Heure d'actualisation", "Name": "Nom du parking", "Status": "Status", "Free": "Place(s) libre(s)", "Total": "Nombre de places"}
	
	endpointsve = {"TAM_MMM_VELOMAG": "velo"}
	idve = {"003": "Esplanade", "005": "Corum"}
	champsve = {"av": "Places occupées", "fr": "Places libres", "to": "Places totales"}
	
	velo = API(url, log=2)
	voiture = API(url, log=2)

	def recup():
		temps = time.strftime("%d/%m/%Y-%H:%M", time.localtime(time.time()))
		
		voiture.downloadEndpoints(endpointsvoi.keys())
		voiture.processXML(champsvoi.keys(), timecap=temps)
		
		velo.downloadEndpoints(endpointsve.keys())
		velo.processXML(champsve.keys(), id=idve.keys(), timecap=temps)

	recup()
	velo.print()
	voiture.print()