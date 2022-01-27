# -*- coding: utf-8 -*-
from recuperer import API, CSV
import statistiques as stat
import time
import os

longueur = 120 #nombre de minute dans un jour
periode = 5 #toutes les 5 minutes

"""
Used to make the dict of velo ids 
re = requests.get("https://data.montpellier3m.fr/sites/default/files/ressources/TAM_MMM_VELOMAG.xml")
tree = etree.fromstring(re.content)
li = list(tree)[0]
res = dict()
for i in li:
	res[i.attrib["id"]] = i.attrib["na"][4:] + " vélo"

print(res)
"""

url = "https://data.montpellier3m.fr/sites/default/files/ressources/{}.xml"

endpoints_voiture = {'FR_MTP_ANTI': 'Antigone voiture', 'FR_MTP_COME': 'Comédie voiture', 'FR_MTP_CORU': 'Corum voiture', 'FR_MTP_EURO': 'Europa voiture', 'FR_MTP_FOCH': 'Foch voiture', 'FR_MTP_GAMB': 'Gambetta voiture', 'FR_MTP_GARE': 'Gare voiture', 'FR_MTP_TRIA': 'Triangle voiture', 'FR_MTP_ARCT': 'Arc de Triomphe voiture', 'FR_MTP_PITO': 'Pitot voiture', 'FR_MTP_CIRC': 'Circe voiture', 'FR_MTP_SABI': 'Sabines voiture', 'FR_MTP_GARC': 'Garcia Lorca voiture', 'FR_MTP_SABL': 'Sablassou voiture', 'FR_MTP_MOSS': 'Mosson voiture', 'FR_STJ_SJLC': 'Saint Jean le Sec voiture', 'FR_MTP_MEDC': 'Euromédecine voiture', 'FR_MTP_OCCI': 'Occitanie voiture', 'FR_CAS_VICA': 'Vicarello voiture', 'FR_MTP_GA109': 'Gaumont EST voiture', 'FR_MTP_GA250': 'Gaumont OUEST voiture', 'FR_CAS_CDGA': 'Charles de Gaulle voiture', 'FR_MTP_ARCE': 'Arceaux voiture', 'FR_MTP_POLY': 'Polygone voiture'}
champs_voiture = {"Status": "Status", "Free": "Place(s) libre(s)", "Total": "Nombre de places"}

endpoints_velo = ["TAM_MMM_VELOMAG"]
id_velo = {'001': 'Rue Jules Ferry - Gare Saint-Roch vélo', '002': 'Comédie vélo', '003': 'Esplanade vélo', '004': 'Hôtel de Ville vélo', '005': 'Corum vélo', '006': 'Place Albert 1er - St Charles vélo', '007': 'Foch vélo', '008': 'Halles Castellane vélo', '009': 'Observatoire vélo', '010': 'Rondelet vélo', '011': 'Plan Cabanes vélo', '012': 'Boutonnet vélo', '013': 'Emile Combes vélo', '014': 'Beaux-Arts vélo', '015': 'Les Aubes vélo', '016': 'Antigone centre vélo', '017': 'Médiathèque Emile Zola vélo', '018': "Nombre d'Or vélo", '019': 'Louis Blanc vélo', '020': 'Gambetta vélo', '021': 'Port Marianne vélo', '022': 'Clemenceau vélo', '023': 'Les Arceaux vélo', '024': 'Cité Mion vélo', '025': 'Nouveau Saint-Roch vélo', '026': 'Renouvier vélo', '027': 'Odysseum vélo', '028': 'Saint-Denis vélo', '029': 'Richter vélo', '030': 'Charles Flahault vélo', '031': 'Voltaire vélo', '032': "Prés d'Arènes vélo", '033': 'Garcia Lorca vélo', '034': 'Vert Bois vélo', '035': 'Malbosc vélo', '036': 'Occitanie vélo', '037': 'FacdesSciences vélo', '038': 'Fac de Lettres vélo', '039': 'Aiguelongue vélo', '040': 'Jeu de Mail des Abbés vélo', '041': 'Euromédecine vélo', '042': 'Marie Caizergues vélo', '043': 'Sabines vélo', '044': 'Celleneuve vélo', '045': 'Jardin de la Lironde vélo', '046': 'Père Soulas vélo', '047': 'Place Viala vélo', '048': 'Hôtel du Département vélo', '049': 'Tonnelles vélo', '050': 'Parvis Jules Ferry - Gare Saint-Roch vélo', '051': 'Pont de Lattes - Gare Saint-Roch vélo', '053': 'Deux Ponts - Gare Saint-Roch vélo', '054': 'Providence - Ovalie vélo', '055': "Pérols Etang de l'Or vélo", '056': 'Albert 1er - Cathédrale vélo', '057': 'Saint-Guilhem - Courreau vélo', '059': 'Sud De France vélo'}
champs_velo = {"av": "Vélos libres", "fr": "Places libres", "to": "Places totales"}

apivoiture = API(url, log=2)
apivelo = API(url, log=2)

def recup():
	temps = time.strftime("%d/%m/%Y-%H:%M", time.localtime(time.time()))

	apivoiture.downloadEndpoints(endpoints_voiture.keys())
	apivoiture.processXML(champs_voiture.keys(), timecap=temps)
	apivoiture.saveCSV(path="./databrutes")

	apivelo.downloadEndpoints(endpoints_velo)
	apivelo.processXML(champs_velo.keys(), id=id_velo.keys(), timecap=temps)
	apivelo.saveCSV(path="./databrutes")

if input(f"Voulez vous lancer un récupération toutes les {periode} minutes pour {longueur} minutes [Y=oui] ? ").lower() == "y":
	apivoiture.runFor(longueur, periode, recup)

"""
def compte_rendu_velo(n, t, m, p, s):
	with open("compte_rendu.txt", "a") as f:
		f.write(f"[{n}]\n")
		f.write(f"	Nombres de vélos disponibles maximum: {t}\n")
		f.write(f"	Moyenne du nombres de vélos disponibles : {m}\n")
		f.write(f"	Pourcentage moyen du nombres de vélos disponibles : {p}%\n")
		f.write(f"	Écart type à la moyenne : {s}\n")
		f.write("\n")
		f.close()

def compte_rendu_voiture(n, t, m, p, s):
	with open("compte_rendu.txt", "a") as f:
		f.write(f"[{n}]\n")
		f.write(f"	Nombres de places disponibles maximum: {t}\n")
		f.write(f"	Moyenne du nombres de places disponibles : {m}\n")
		f.write(f"	Pourcentage moyen du nombres de places disponibles : {p}%\n")
		f.write(f"	Écart type à la moyenne : {s}\n")
		f.write("\n")
		f.close()

recupvelo  = CSV(id_velo.keys(), path="./databrutes")
recupvoiture = CSV(endpoints_voiture.keys(), path="./databrutes")

code_park = list(endpoints_voiture.keys())[0]
data_corum = recupvoiture.getOne(code_park)
total =  data_corum["Total"][0]
moyenne = stat.moyenne(data_corum["Free"])
sigma = stat.ecart_type(data_corum["Free"])
pourcent = stat.pourcentage(moyenne, total)
compte_rendu_voiture(f"{endpoints_voiture[code_park]}", total, moyenne, pourcent, sigma)

data_velo = recupvelo.getFromList(id_velo.keys())
for code, nom in id_velo.items():
	total =  data_velo[code]["to"][0]
	moyenne = stat.moyenne(data_velo[code]["av"])
	sigma = stat.ecart_type(data_velo[code]["av"])
	pourcent = stat.pourcentage(moyenne, total)
	compte_rendu_velo(f"{nom}", total, moyenne, pourcent, sigma)

for code, nom in id_velo.items():
	co = stat.covar(data_corum["Free"], data_velo[code]["av"])
	t = stat.ecart_type(data_corum["Free"]) * stat.ecart_type(data_velo[code]["av"])
	with open("compte_rendu.txt", "a") as f:
		f.write(f"[Covariance {endpoints_voiture[code_park]} / {nom}]\n")
		f.write(f"	Covariance : {co}\n")
		f.write(f"	Coefficient de corrélation : {round(co/t, 2)}\n")
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
"""
