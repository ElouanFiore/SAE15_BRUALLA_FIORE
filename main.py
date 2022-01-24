from recuperer import API

url = "https://data.montpellier3m.fr/sites/default/files/ressources/{}.xml"
endpoints = {'FR_MTP_ANTI': 'Antigone', 'FR_MTP_COME': 'Comédie', 'FR_MTP_CORU': 'Corum', 'FR_MTP_EURO': 'Europa', 'FR_MTP_FOCH': 'Foch', 'FR_MTP_GAMB': 'Gambetta', 'FR_MTP_GARE': 'Gare', 'FR_MTP_TRIA': 'Triangle', 'FR_MTP_ARCT': 'Arc de Triomphe', 'FR_MTP_PITO': 'Pitot', 'FR_MTP_CIRC': 'Circe', 'FR_MTP_SABI': 'Sabines', 'FR_MTP_GARC': 'Garcia Lorca', 'FR_MTP_SABL': 'Sablassou', 'FR_MTP_MOSS': 'Mosson', 'FR_STJ_SJLC': 'Saint Jean le Sec', 'FR_MTP_MEDC': 'Euromédecine', 'FR_MTP_OCCI': 'Occitanie', 'FR_CAS_VICA': 'Vicarello', 'FR_MTP_GA109': 'Gaumont EST', 'FR_MTP_GA250': 'Gaumont OUEST', 'FR_CAS_CDGA': 'Charles de Gaulle', 'FR_MTP_ARCE': 'Arceaux', 'FR_MTP_POLY': 'Polygone'}
champs = {"DateTime": "Heure d'actualisation", "Name": "Nom du parking", "Status": "Status", "Free": "Place(s) libre(s)", "Total": "Nombre de places"}
parkings = API(url)

def recup():
	parkings.downloadEndpoints(endpoints.keys())
	parkings.processXML(champs.keys())
	parkings.saveCSV()
	parkings.print()

recup()
data = {}

for code in endpoints.keys():
	data[code] = {}

	with open(f"{code}.csv") as fichier:
		temp = fichier.read()
		fichier.close()
	
	temp = temp.split("\n")
	for i, val in enumerate(temp):
		temp[i] = val.split(";")
	temp = temp[1:-1]

	for i, champ in enumerate(champs.keys()):
		data[code][champ] = [] 
		for val in temp:
			data[code][champ].append(val[i])

print(data)
