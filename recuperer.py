<<<<<<< HEAD
#:!/usr/bin/python3
# Elouan FIORE
=======
# Elouan FIORE Léo BRUALLA
>>>>>>> 6ca9708d58fc09a127754b581278b21335c6a815
# Version 1


from lxml import etree
import requests
import time

class API():
	def __init__(self, url, where="tag", log=1):
		self.url = url
		self.loglevel = log
		self.where = where
	
	def downloadEndpoints(self, endpoints):
		error = 0
		if self.where == "id":
			self.endpoints = endpoints
			self.log(2, f"Downloading {self.url}...")
			
			reponse = requests.get(self.url)
			status = reponse.status_code
			if status == 200:
				self.endpointsData = reponse.content
			else:
				error += 1
				self.log(0, f"Error {status}")

		elif self.where == "tag":
			self.endpointsData = {}

			for code in endpoints:
				self.log(2, f"Downloading {code}...")

				reponse = requests.get(self.url.format(code))
				status = reponse.status_code

				if status == 200:
					self.endpointsData[code] = reponse.content
				else:
					error += 1
					self.log(0, f"Error {status}")
		
		self.log(1, f"########## End downloading, {error} error(s) ##########\n")
	

	def processXML(self, field, timecap=0):
		if self.where == "tag":
			self.endpointsParse = {}
			for code, contenu in self.endpointsData.items():
				self.log(2, f"Converting {code}...")
				contenu = etree.fromstring(contenu)	

				self.log(2, f"Processing {code}...")
				self.endpointsParse[code] = {}

				if timecap == 0:
					now = time.localtime(time.time())
					timecap = time.strftime("%d/%m/%Y-%H:%M", now)
				self.endpointsParse[code]["CapTime"] = timecap

				for f in field:
					for i in contenu:
						if i.tag == f:
							self.endpointsParse[code][f] = i.text

			self.log(1, f"########## End processing ##########\n")
	
		elif self.where == "id":
			self.endpointsParse = {}
			self.log(2, f"Converting {self.url}...")
			contenu = etree.fromstring(self.endpointsData)
			
			#pass the first element which is a <sl> tag empty
			contenu = list(contenu)[0]


			for code in self.endpoints:
				self.log(2, f"Processing {code}...")
				self.endpointsParse[code] = {}

				if timecap == 0:
					now = time.localtime(time.time())
					timecap = time.strftime("%d/%m/%Y-%H:%M", now)
				self.endpointsParse[code]["CapTime"] = timecap

				for element in contenu:
					attr = element.attrib
					if attr["id"] == code:
						for f in field:
							self.endpointsParse[code][f] = attr[f]
						

			self.log(1, f"########## End processing ##########\n")

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
		
		self.log(1, "########## End saving ##########\n")
	
	def print(self):
		for code, contenu in self.endpointsParse.items():
			print(f"\n{code}")
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
			self.log(1, f"########## Sleeping for {sleep/60} min ##########\n")
			time.sleep(sleep - execTime)
		
		self.log(1, f"Executed {execute} time(s)")
	
	def log(self, level, message):
		if self.loglevel >= level:
			print(message)
			with open("recup.log", "a") as f:
				f.write(f"\n{message}")
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
	urlvoi = "https://data.montpellier3m.fr/sites/default/files/ressources/{}.xml"
	endpointsvoi = {'FR_MTP_ANTI': 'Antigone', 'FR_MTP_COME': 'Comédie', 'FR_MTP_CORU': 'Corum', 'FR_MTP_EURO': 'Europa', 'FR_MTP_FOCH': 'Foch', 'FR_MTP_GAMB': 'Gambetta', 'FR_MTP_GARE': 'Gare', 'FR_MTP_TRIA': 'Triangle', 'FR_MTP_ARCT': 'Arc de Triomphe', 'FR_MTP_PITO': 'Pitot', 'FR_MTP_CIRC': 'Circe', 'FR_MTP_SABI': 'Sabines', 'FR_MTP_GARC': 'Garcia Lorca', 'FR_MTP_SABL': 'Sablassou', 'FR_MTP_MOSS': 'Mosson', 'FR_STJ_SJLC': 'Saint Jean le Sec', 'FR_MTP_MEDC': '    Euromédecine', 'FR_MTP_OCCI': 'Occitanie', 'FR_CAS_VICA': 'Vicarello', 'FR_MTP_GA109': 'Gaumont EST', 'FR_MTP_GA250': 'Gaumont OUEST', 'FR_CAS_CDGA': 'Charles de Gaulle', 'FR_MTP_ARCE': 'Arceaux', 'FR_MTP_POLY': 'Polygone'}
	champsvoi = {"DateTime": "Heure d'actualisation", "Name": "Nom du parking", "Status": "Status", "Free": "Place(s) libre(s)", "Total": "Nombre de places"}
	voiture = API(urlvoi, log=2)
	
	urlve = "https://data.montpellier3m.fr/sites/default/files/ressources/TAM_MMM_VELOMAG.xml"
	endpointsve = {"003": "Esplanade", "005": "Corum"}
	champsve = {"av": "Places occupées", "fr": "Places libres", "to": "Places totales"}
	velo = API(urlve, where="id", log=2)

	def recup():
		temps = time.strftime("%d/%m/%Y-%H:%M", time.localtime(time.time()))
		voiture.downloadEndpoints(endpointsvoi.keys())
		voiture.processXML(champsvoi.keys(), timecap=temps)
		voiture.saveCSV(path="./databrutes")
		velo.downloadEndpoints(endpointsve.keys())
		velo.processXML(champsve.keys(), timecap=temps)
		velo.saveCSV(path="./databrutes")

	recup()

	revoiture = CSV(endpointsve.keys(), path="./databrutes")
	print(revoiture.getFromList(endpointsve.keys()))
