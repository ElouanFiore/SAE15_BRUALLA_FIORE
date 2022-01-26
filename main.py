# -*- coding: utf-8 -*-
from recuperer import API, CSV
import statistiques as stat
import time
import os

url = "https://data.montpellier3m.fr/sites/default/files/ressources/{}.xml"

endpoints_voiture = {'FR_MTP_CORU': 'Corum voiture'}
champs_voiture = {"Status": "Status", "Free": "Place(s) libre(s)", "Total": "Nombre de places"}

endpoints_velo = {"TAM_MMM_VELOMAG": "velo"}
id_velo = {"003": "Esplanade vélo", "005": "Corum vélo"}
champs_velo = {"av": "Places occupées", "fr": "Places libres", "to": "Places totales"}

voiture = API(url, log=2)
velo = API(url, log=2)

def recup():
	temps = time.strftime("%d/%m/%Y-%H:%M", time.localtime(time.time()))

	voiture.downloadEndpoints(endpoints_voiture.keys())
	voiture.processXML(champs_voiture.keys(), timecap=temps)
	voiture.saveCSV(path="./databrutes")

	velo.downloadEndpoints(endpoints_velo.keys())
	velo.processXML(champs_velo.keys(), id=id_velo.keys(), timecap=temps)
	velo.saveCSV(path="./databrutes")

def compte_rendu(n, t, m, p, s):
	with open("compte_rendu.txt", "a") as f:
		f.write(f"[{n}]\n")
		f.write(f"	Nombres de vélos disponible maximum: {t}\n")
		f.write(f"	Moyenne du nombres de vélos disponibles : {m}\n")
		f.write(f"	Pourcentage moyen du nombres de vélos disponibles : {p}%\n")
		f.write(f"	Ecart type à la moyenne : {s}\n")
		f.write("\n")
		f.close()

if input("Voulez-vous lancez une récupération ? [Y = oui ] ").lower() == "y":
	recup()

recupvelo  = CSV(id_velo.keys(), path="./databrutes")
recupvoiture = CSV(endpoints_voiture.keys(), path="./databrutes")

code_park = list(endpoints_voiture.keys())[0]
data_corum = recupvoiture.getOne(code_park)
total =  data_corum["Total"][0]
moyenne = stat.moyenne(data_corum["Free"])
sigma = stat.ecart_type(data_corum["Free"])
pourcent = stat.pourcentage(moyenne, total)
compte_rendu(f"{endpoints_voiture[code_park]}", total, moyenne, pourcent, sigma)

data_velo = recupvelo.getFromList(id_velo.keys())
for code, nom in id_velo.items():
	total =  data_velo[code]["to"][0]
	moyenne = stat.moyenne(data_velo[code]["av"])
	sigma = stat.ecart_type(data_velo[code]["av"])
	pourcent = stat.pourcentage(moyenne, total)
	compte_rendu(f"{nom}", total, moyenne, pourcent, sigma)

for code, nom in id_velo.items():
	co = stat.covar(data_corum["Free"], data_velo[code]["av"])
	t = stat.ecart_type(data_corum["Free"]) * stat.ecart_type(data_velo[code]["av"])
	with open("compte_rendu.txt", "a") as f:
		f.write(f"[Covariance {endpoints_voiture[code_park]} / {nom}]\n")
		f.write(f"	Covariance : {co}\n")
		f.write(f"	Indice de covariance : {round(co/t, 2)}\n")
		f.write("\n")
		f.close()


stat.datagnuplot(data_corum["CapTime"], data_corum["Free"], data_velo["003"]["av"], data_velo["005"]["av"])

nom1 = endpoints_voiture[code_park]
nom2 = id_velo["003"]
nom3 = id_velo["005"]

with open("conf.plot", "w") as f:
	f.write("reset\nset title 'Vélos et places de parkings disponibles en fonction du temps'\n")
	f.write("set xdata time\nset timefmt '%d/%m/%Y-%H:%M'\nset format x '%H:%M'\nset xlabel 'Heure de la journée du 24/01/2022 et 25/02/2022'\n")
	f.write("set ylabel 'Place de parkings disponibles'\n")
	f.write("set y2tics\nset y2range [2:17]\nset y2label 'Vélos disponibles'\n")
	f.write("set terminal png size 2000,1000 enhanced\nset output 'graph.png'\n")
	f.write(f"plot 'forgnuplot.dat' using 1:2 with lines title '{nom1}', 'forgnuplot.dat' using 1:3 with lines axes x1y2 title '{nom2}', 'forgnuplot.dat' using 1:4 with lines axes x1y2 title '{nom3}'\n")
	f.close()

os.system("gnuplot conf.plot")