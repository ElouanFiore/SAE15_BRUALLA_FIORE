# -*- coding: utf-8 -*-
from recuperer import API, CSV
import statistiques as stat
import time
import os

longueur = 24*60 #nombre de minute dans un jour
periode = 5 #toutes les 5 minutes

"""
Utilisé pour récupéré les ids des parkings vélo
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
	"""
	La récupération qui sera effectué
	"""
	temps = time.strftime("%d/%m/%Y-%H:%M", time.localtime(time.time()))

	apivoiture.downloadEndpoints(endpoints_voiture.keys())
	apivoiture.processXML(champs_voiture.keys(), timecap=temps)
	apivoiture.saveCSV(path="./databrutes")

	apivelo.downloadEndpoints(endpoints_velo)
	apivelo.processXML(champs_velo.keys(), id=id_velo.keys(), timecap=temps)
	apivelo.saveCSV(path="./databrutes")

def compte_rendu_velo(n, t, m, p, s):
	with open("compte_rendu.txt", "a", encoding="utf8") as f:
		f.write(f"[{n}]\n")
		f.write(f"	Nombres de vélos disponibles maximum: {t}\n")
		f.write(f"	Moyenne du nombres de vélos disponibles : {m}\n")
		f.write(f"	Pourcentage moyen du nombres de vélos disponibles : {p}%\n")
		f.write(f"	Écart type à la moyenne : {s}\n")
		f.write("\n")
		f.close()

def compte_rendu_voiture(n, t, m, p, s):
	with open("compte_rendu.txt", "a", encoding="utf8") as f:
		f.write(f"[{n}]\n")
		f.write(f"	Nombres de places disponibles maximum: {t}\n")
		f.write(f"	Moyenne du nombres de places disponibles : {m}\n")
		f.write(f"	Pourcentage moyen du nombres de places disponibles : {p}%\n")
		f.write(f"	Écart type à la moyenne : {s}\n")
		f.write("\n")
		f.close()

if input(f"Voulez vous lancer un récupération toutes les {periode} minutes pour {longueur} minutes [Y=oui] ? ").lower() == "y":
	apivoiture.runFor(longueur, periode, recup)

recupvoiture = CSV(endpoints_voiture.keys(), path="./databrutes")
recupvelo = CSV(id_velo.keys(), path="./databrutes")
datavoiture = recupvoiture.getFromList(endpoints_voiture.keys()) 
datavelo = recupvelo.getFromList(id_velo.keys())

#Calcul la moyenne de vélos/places libres
moyenne_libre = dict()
for f in endpoints_voiture.keys():
	moyenne_libre[f] = stat.moyenne(datavoiture[f]["Free"])
for f in id_velo.keys():
	moyenne_libre[f] = stat.moyenne(datavelo[f]["av"])

#Calcul le pourcentage moyen de vélos/places libres
pourcentage_libre = dict()
for f in endpoints_voiture.keys():
	pourcentage_libre[f] = stat.pourcentage(moyenne_libre[f], datavoiture[f]["Total"][0])
for f in id_velo.keys():
	pourcentage_libre[f] = stat.pourcentage(moyenne_libre[f], datavelo[f]["to"][0])

#Calcul l'écart type à la moyenne des vélos/places libres
ecart_type = dict()
for f in endpoints_voiture.keys():
	ecart_type[f] = stat.ecart_type(datavoiture[f]["Free"])
for f in id_velo.keys():
	ecart_type[f] = stat.ecart_type(datavelo[f]["av"])

#Calcul le nombre de places/vélos libre sur tout les parkings par mesure
velo_libre = []
place_libre = []
for i in range(int(longueur/periode)):
	for f in endpoints_voiture.keys():
		if i == len(place_libre):
			place_libre.append(int(datavoiture[f]["Free"][i]))
		else:
			place_libre[i] += int(datavoiture[f]["Free"][i])
	for f in id_velo.keys():
		if i == len(velo_libre):
			velo_libre.append(int(datavelo[f]["av"][i]))
		else:
			velo_libre[i] += int(datavelo[f]["av"][i])

#Calcul la moyenne de vélos/places libres sur tout les parkings
velo_libre_mo = stat.moyenne(velo_libre)
place_libre_mo = stat.moyenne(place_libre)

#Calcul l'écart type à la moyenne des vélos/places libres sur tout les parkings
velo_libre_si = stat.ecart_type(velo_libre)
place_libre_si = stat.ecart_type(place_libre)

#Calcul le nombre de places/velos total disponible sur tout les parkings
velo_total = 0
place_total = 0
for f in endpoints_voiture.keys():
	place_total += int(datavoiture[f]["Total"][0])
for f in id_velo.keys():
	velo_total += int(datavelo[f]["to"][0])

#Ecrit les valeurs trouvé dans le compte rendu
for f, n in endpoints_voiture.items():
	compte_rendu_voiture(n, int(datavoiture[f]["Total"][0]), moyenne_libre[f], pourcentage_libre[f], ecart_type[f])
for f, n in id_velo.items():
	compte_rendu_velo(n, int(datavelo[f]["to"][0]), moyenne_libre[f], pourcentage_libre[f], ecart_type[f])
compte_rendu_voiture("Total places", place_total, place_libre_mo, stat.pourcentage(place_libre_mo, place_total), place_libre_si)
compte_rendu_velo("Total vélos", velo_total, velo_libre_mo, stat.pourcentage(velo_libre_mo, velo_total), velo_libre_si)



#Calcul l'indice de correlation entre chaques parking vélo et voiture
indice_correlation = dict()
with open("heatmap.dat", "w", encoding="utf8") as h:
	header = ",".join(list(id_velo.keys()))
	h.write(f",{header}\n")
	for f in endpoints_voiture.keys():
		indice_correlation[f] = dict()
		line = f.replace("_", "\\\\_") #Permet de ne pas compter "_" comme un caractère qui a un effet sur le texte 
		for i in id_velo.keys():
			if ecart_type[f] == 0 or ecart_type[i] == 0: #Pour eviter les erreurs de division par 0
				indice_correlation[f][i] = 0
				line += ",0"
			else:
				indice_correlation[f][i] = stat.covar(datavoiture[f]["Free"], datavelo[i]["av"]) / (ecart_type[f]*ecart_type[i])
				line += f",{indice_correlation[f][i]}"
		h.write(f"{line}\n")
	h.close()

os.system("gnuplot heatmap.plot")

#Trouve le plus fort indice de corrélation
graph = [0, 0, 0]
for f in endpoints_voiture.keys():
	for i in id_velo.keys():
		if graph[0] < indice_correlation[f][i]:
			graph[0], graph[1], graph[2] = indice_correlation[f][i], f, i
graph[0] = round(graph[0], 4)

#Créé le graphique des 2 parkings avec le plus fort indice de corrélation
with open("graph.dat", "w", encoding="utf8") as f:
	for i, val in enumerate(datavoiture[graph[1]]["CapTime"]):
		a = val
		b = datavoiture[graph[1]]["Free"][i]
		c = datavelo[graph[2]]["av"][i]
		f.write(f"{a} {b} {c}\n")

with open("graph.plot", "w", encoding="utf8") as f:
	f.write(f"set title 'Vélos et places de parkings disponibles des parkings les plus corrélé ({graph[0]}) en fonction du temps'\n")
	f.write("set xdata time\nset timefmt '%d/%m/%Y-%H:%M'\nset format x '%H:%M'\nset xlabel 'Heure de la journée du 27/01/2022 et 28/02/2022'\n")
	f.write("set ylabel 'Places de parkings disponibles'\n")
	f.write("set y2tics\nset y2range [2:17]\nset y2label 'Vélos disponibles'\n")
	f.write("set terminal png size 2000,1000 enhanced\nset output 'graph.png'\n")
	f.write(f"plot 'graph.dat' using 1:2 with lines title '{endpoints_voiture[graph[1]]}', 'graph.dat' using 1:3 with lines axes x1y2 title '{id_velo[graph[2]]}'\n")
	f.close()

os.system("gnuplot graph.plot")
