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

if input("Voulez-vous lancez une récupération ? [Y = oui ] ").lower() == "y":

	def recup():
		temps = time.strftime("%d/%m/%Y-%H:%M", time.localtime(time.time()))
	
		voiture.downloadEndpoints(endpoints_voiture.keys())
		voiture.processXML(champs_voiture.keys(), timecap=temps)
		voiture.saveCSV(path="./databrutes")
	
		velo.downloadEndpoints(endpoints_velo.keys())
		velo.processXML(champs_velo.keys(), timecap=temps)
		velo.saveCSV(path="./databrutes")

	velo.runFor(1440, 5, recup)


recupvelo  = CSV(endpoints_velo.keys(), path="./databrutes")
data_velo = recupvelo.getFromList(endpoints_velo.keys())

for i in endpoints.velo.keys[]:
	total =  data_velo[i]["to"]
	moyenne = stat.moyenne(data_velo[i]["av"])
	sigma = stat.ecart_type(data_velo[i]["av"])
	pourcent = stat.pourcentage(moyenne, total)
	
	with open("compte_rendu.txt", "a") as f:
		f.writeline(f"[{endpoints_velo[i]}]")
		f.writeline(f"	Nombres de vélos disponible maximum: {total}")
		f.writeline(f"	Moyenne du nombres de vélos disponibles : {moyenne}")
		f.writeline(f"	Pourcentage moyen du nombres de vélos disponibles : {pourcent}")
		f.writeline(f"	Ecart type à la moyenne : {sigma}")

recupvoiture = CSV(endpoints_voiture.keys(), path="./databrutes")
code_park = list(endpoints_voiture.keys())[0]
data_corum = recupvoiture.getOne(code_park)

total =  data_corum["Total"]
moyenne = stat.moyenne(data_corum[i]["Free"])
sigma = stat.ecart_type(data_corum[i]["Free"])
pourcent = stat.pourcentage(moyenne, total)

with open("compte_rendu.txt", "a") as f:
	f.writeline(f"[{endpoints_voiture[code_park]}]")
	f.writeline(f"	Nombres de vélos disponible maximum: {total}")
	f.writeline(f"	Moyenne du nombres de vélos disponibles : {moyenne}")
	f.writeline(f"	Pourcentage moyen du nombres de vélos disponibles : {pourcent}")
	f.writeline(f"	Ecart type à la moyenne : {sigma}")
