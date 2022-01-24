from recuperer import API, CSV

urlvelo = "https://data.montpellier3m.fr/sites/default/files/ressources/{}.xml"
endpoints = {'FR_MTP_ANTI': 'Antigone', 'FR_MTP_COME': 'Comédie', 'FR_MTP_CORU': 'Corum', 'FR_MTP_EURO': 'Europa', 'FR_MTP_FOCH': 'Foch', 'FR_MTP_GAMB': 'Gambetta', 'FR_MTP_GARE': 'Gare', 'FR_MTP_TRIA': 'Triangle', 'FR_MTP_ARCT': 'Arc de Triomphe', 'FR_MTP_PITO': 'Pitot', 'FR_MTP_CIRC': 'Circe', 'FR_MTP_SABI': 'Sabines', 'FR_MTP_GARC': 'Garcia Lorca', 'FR_MTP_SABL': 'Sablassou', 'FR_MTP_MOSS': 'Mosson', 'FR_STJ_SJLC': 'Saint Jean le Sec', 'FR_MTP_MEDC': 'Euromédecine', 'FR_MTP_OCCI': 'Occitanie', 'FR_CAS_VICA': 'Vicarello', 'FR_MTP_GA109': 'Gaumont EST', 'FR_MTP_GA250': 'Gaumont OUEST', 'FR_CAS_CDGA': 'Charles de Gaulle', 'FR_MTP_ARCE': 'Arceaux', 'FR_MTP_POLY': 'Polygone'}
champs = {"Status": "Status", "Free": "Place(s) libre(s)", "Total": "Nombre de places"}
"""
voiture = API(url, 2)

def recup():
	voiture.downloadEndpoints(endpoints.keys())
	voiture.processXML(champs.keys())
	voiture.saveCSV()
	voiture.print()

recup()
"""

parkings = CSV(endpoints.keys())
parkings.getAll()
