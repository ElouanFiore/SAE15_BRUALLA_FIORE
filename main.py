from recuperer import API, CSV
import time
import statistiques as stat

url_voiture = "https://data.montpellier3m.fr/sites/default/files/ressources/{}.xml"
endpoints_voiture = {'FR_MTP_CORU': 'Corum'}
champs_voiture = {"Status": "Status", "Free": "Place(s) libre(s)", "Total": "Nombre de places"}
voiture = API(url_voiture, log=2)

url_velo = "https://data.montpellier3m.fr/sites/default/files/ressources/TAM_MMM_VELOMAG.xml"
endpoints_velo = {"003": "Esplanade", "005": "Corum"}
champs_velo = {"av": "Places occupées", "fr": "Places libres", "to": "Places totales"}
velo = API(url_velo, where="id", log=2)

if input("Voulez-vous lancez une récupération ? [Y = oui ]").lower() == "y":

	def recup():
		temps = time.strftime("%d/%m/%Y-%H:%M", time.localtime(time.time()))
	
		voiture.downloadEndpoints(endpoints_voiture.keys())
		voiture.processXML(champs_voiture.keys(), timecap=temps)
		voiture.saveCSV(path="./databrutes")
	
		velo.downloadEndpoints(endpoints_velo.keys())
		velo.processXML(champs_velo.keys(), timecap=temps)
		velo.saveCSV(path="./databrutes")

	velo.runFor(1440, 5, recup)


revelo  = CSV(endpoints_velo.keys(), path="./databrutes")
revoiture = CSV(endpoints_voiture.keys(), path="./databrutes")
data_velo = revelo.getFromList(endpoints_velo.keys())
data_voiture =revoiture.getOne(list(endpoints_voiture.keys())[0])

print("Moyenne voiture tqt", stat.moyenne(data_voiture["Free"]))
print("Moyenne velo 005 tqt", stat.moyenne(data_velo["005"]["fr"]))
print("Ecart type voiture tqt", stat.ecart_type(data_voiture["Free"]))
