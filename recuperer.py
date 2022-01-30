# -*- coding: utf-8 -*-
# Elouan FIORE Léo BRUALLA
# Version 1

import lxml.etree
import requests
import time

class API():
	"""
	Permet de récupérer plusieurs données dans des fichiers sur internet
	"""
	def __init__(self, url, log=1):
		self.url = url
		self.loglevel = log
		self.endpointsParse = {}

	def downloadEndpoints(self, lst=[]):
		"""
		Télécharges les fichiers selon une liste et l'url qui lui à été donné
		"""
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
		"""
		Traite les fichier récupéré pour avoir les données selon une liste de champs spécifié
		"""
		self.field = list(field)
		if timecap == 0: #Gère lui même la marque de temps si elle n'est pas spécifié
			now = time.localtime(time.time())
			timecap = time.strftime("%d/%m/%Y-%H:%M", now)

		if id == []: #Traite les champs par le tag des balises
			for code, contenu in self.endpointsData.items():
				self.log(2, f"Converting {code}...")
				try: 
					contenu = lxml.etree.fromstring(contenu)	
				except lxml.etree.XMLSyntaxError: #Permet de ne pas stopper le programme si doc vide
					self.log(0, f"PARSING ERROR {code}")
					if not code in self.endpointsParse.keys():
						self.endpointsParse[code] = {"CapTime": timecap}
					else: # Réutilise les dernières données si elles existent
						self.endpointsParse[code]["CapTime"] = timecap
						print(self.endpointsParse)
				
				else:
					self.log(2, f"Processing {code}...")
					self.endpointsParse[code] = {}
					self.endpointsParse[code]["CapTime"] = timecap
					for f in field:
						for i in contenu:
							if i.tag == f:
								self.endpointsParse[code][f] = i.text
		
		else: #Traite les champs par l'id des balises
			for code, contenu in self.endpointsData.items():
				self.log(2, f"Converting {code}...")
				try: 
					contenu = lxml.etree.fromstring(contenu)
				except lxml.etree.XMLSyntaxError: #Permet de ne pas stopper le programme si doc vide
					self.log(0, f"PARSING ERROR {code}")
					for i in id:
						if not i in self.endpointsParse.keys():
							self.endpointsParse[i] = {"CapTime": timecap}
						else: # Réutilise les dernières données si elles existent
							self.endpointsParse[i]["CapTime"] = timecap
				else:
					contenu = list(contenu)[0] #Passe le premier élément qui est vide
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
		"""
		Sauvegarde les données traité en format CSV
		"""
		for code, contenu in self.endpointsParse.items():
			self.log(2, f"Saving {code}...")
			line = ""
			for data in contenu.values(): # Créé la ligne à écrire
				line += f"{data};"
			
			try:
				fichier = open(f"{path}/{code}.csv", "r")
				fichier.close()
			except FileNotFoundError: #Créé les headers si le fichier n'existe pas
				header = ";".join(["CapTime"] + self.field)
				with open(f"{path}/{code}.csv", "w") as fichier:
					fichier.write(f"{header}\n{line}\n")
					fichier.close()
			else:
				with  open(f"{path}/{code}.csv", "a") as fichier:
					fichier.write(f"{line}\n")
					fichier.close()
		
		self.log(1, "######################################### End saving ##########################################")
	
	def print(self):
		"""
		Fonction qui a surtout été utilisé pendant le développement
		"""
		for code, contenu in self.endpointsParse.items():
			print(f"{code}")
			for field, data in contenu.items():
				print(f"	{field} : {data}")

	def runFor(self, lenght, sleep, function):
		"""
		Fonction qui permet de programmer la longueur de la récupération et la fréquences des récupérations
		"""
		endTime = int(time.time()) + lenght*60
		execute = 0
		sleep *= 60
		endstr =time.strftime("%d/%m/%Y %H:%M", time.localtime(endTime))
		self.log(1, f"End at {endstr}")
		while int(time.time()) < endTime:
			execTime = int(time.time())
			function()
			execute += 1
			
			if int(time.time()) < endTime:
				self.log(1, f"#################################### Sleeping for {sleep/60} min #####################################")
				execTime = int(time.time()) - execTime #Permet de connaître la longuer de l'éxécution pour la soustraire à la longueur du sleep
				time.sleep(sleep - execTime)
		
		self.log(1, f"Executed {execute} time(s)")
	
	def log(self, level, message):
		"""
		Fonction de log avec 3 niveaux
		0 rien sauf les erreurs
		1 les erreurs et les grandes étapes (par défaut)
		2 les erreurs et à quel endpoint le programme en est
		"""
		now = time.localtime(time.time())
		message = time.strftime("%d/%m/%Y %H:%M:%S ; ", now) + message
		if self.loglevel >= level:
			print(message)
			with open("recup.log", "a") as f:
				f.write(f"{message}\n")
				f.close()

class CSV():
	def __init__(self, name, path="."):
		"""
		Classe qui sert de parseur CSV fait maison
		"""
		self.name = name
		self.data = {}
		self.dataparsed = {}
	
		for code in self.name:
			with open(f"{path}/{code}.csv", "r") as f:
				self.data[code] = f.read()
				f.close()
	
	def getOne(self, code):
		"""
		Retourne les données d'un fichier dans un dictionnaire contenant des listes selon les headers
		""" 
		if code in self.dataparsed.keys(): #Cherhce si le fichier à déjà été parsé
			return self.dataparsed[code]
		
		else:
			parsed = {}
			
			self.data[code] = self.data[code].split("\n") #Sépare les lignes
			for index, val in enumerate(self.data[code]):
				self.data[code][index] = val.split(";") #Sépare les données
			
			for index, field in enumerate(self.data[code][0]): #Parcour le fichier selon les headers
				parsed[field] = []
				
				for line in range(1, len(self.data[code])-1): #Passe le header et la dernière ligne vide
					parsed[field].append(self.data[code][line][index])

			self.dataparsed[code] = parsed #Ajoute le fichier aux fichiers parsés
			return parsed
	
	def getFromList(self, list):
		"""
		Retourne les données de plusieurs fichiers dans un dictionnaire contenant les fichiers sous forme de dictionaires contenant des listes selon les headers
		""" 
		listparsed = {}
		
		for code in list:
			if code in self.dataparsed.keys(): #Cherhce si le fichier à déjà été parsé
				listparsed[code] = self.dataparsed[code]
			
			else:
				listparsed[code] = {}
				
				self.data[code] = self.data[code].split("\n")  #Sépare les lignes
				for index, val in enumerate(self.data[code]):
					self.data[code][index] = val.split(";") #Sépare les données

				for index, field in enumerate(self.data[code][0]): #Parcour le fichier selon les headers
					listparsed[code][field] =  []
					
					for line in range(1, len(self.data[code])-1): #Passe le header et la dernière ligne vide
						listparsed[code][field].append(self.data[code][line][index])

				self.dataparsed[code] = listparsed[code] #Ajoute le fichier aux fichiers parsés

		return listparsed