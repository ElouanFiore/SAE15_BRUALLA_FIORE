# Présentation des données

- [Présentation des données](#présentation-des-données)
  - [**Emplacement**](#emplacement)
    - [**Données brutes :**](#données-brutes-)
    - [**Données traités :**](#données-traités-)
  - [**Analyse**](#analyse)
    - [**Définitions**](#définitions)
      - [Facteur de corrélation](#facteur-de-corrélation)
      - [Ecart Type](#ecart-type)
    - [**Correspondances parkings vélos**](#correspondances-parkings-vélos)
    - [**Carte de température**](#carte-de-température)
    - [**Les plus corrélé**](#les-plus-corrélé)
    - [**Données totales**](#données-totales)

## **Emplacement**
### **Données brutes :**
Toutes les données brutes sont disponibles dans le repertoire databrutes au format CSV.

### **Données traités :**
Les données les plus interessantes sont dans le fichier [compte_rendu.txt](https://raw.githubusercontent.com/ElouanFiore/SAE15_BRUALLA_FIORE/main/compte_rendu.txt), il contient pour chaque parkings :
1. Le nombre de places/vélos disponibles au maximum
2. La moyenne de places/vélos libres
3. Le pourcentage moyen de places/vélos libres sur le temps de mesure.
4. L'écart type à cette moyenne 

Les mêmes données pour tout les parkings voitures réunis et tout les parkings vélos réunis sont à la fin du compte rendu.

## **Analyse**
### **Définitions**
#### Facteur de corrélation :
Peut démontrer une corrélation entre deux courbes, si elles évoluent dans le même sens le facteur se rapproche de 1, si elles évoluent dans des sens contraire le facteur se rapproche de -1 et si elles n'ont rien à voir le facteur se rapproche de 0. C'est un outil qui permet un analyse, il ne démontre en aucun cas une corrélation à 100%.

#### Écart Type :
Complémentaire à la moyenne il permet de savoir comment les valeurs sont dispersé autour de cette moyenne. Une courbe avec un écart type élevé aura plus de fluctuations autour de la moyenne qu'une courbe avec la même moyenne mais un écart type plus petit.

### **Correspondances parkings vélos**
001|002|003|004|005|006|007|008|009|010|011|012|013|014|015|016|017|018|019|020|021|022|023|024|025|026|027|028
-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-
Rue Jules Ferry - Gare Saint-Roch vélo|Comédie vélo|Esplanade vélo|Hôtel de Ville vélo|Corum vélo|Place Albert 1er - St Charles vélo|Foch vélo|Halles Castellane vélo|Observatoire vélo|Rondelet vélo|Plan Cabanes vélo|Boutonnet vélo|Emile Combes vélo|Beaux-Arts vélo|Les Aubes vélo|Antigone centre vélo|Médiathèque Emile Zola vélo|Nombre d'Or vélo|Louis Blanc vélo|Gambetta vélo|Port Marianne vélo|Clemenceau vélo|Les Arceaux vélo|Cité Mion vélo|Nouveau Saint-Roch vélo|Renouvier vélo|Odysseum vélo|Saint-Denis vélo|

029|030|031|032|033|034|035|036|037|038|039|040|041|042|043|044|045|046|047|048|049|050|051|053|054|055|056|057|059
-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-
Richter vélo|Charles Flahault vélo|Voltaire vélo|Prés d'Arènes vélo|Garcia Lorca vélo|Vert Bois vélo|Malbosc vélo|Occitanie vélo|FacdesSciences vélo|Fac de Lettres vélo|Aiguelongue vélo|Jeu de Mail des Abbés vélo|Euromédecine vélo|Marie Caizergues vélo|Sabines vélo|Celleneuve vélo|Jardin de la Lironde vélo|Père Soulas vélo|Place Viala vélo|Hôtel du Département vélo|Tonnelles vélo|Parvis Jules Ferry - Gare Saint-Roch vélo|Pont de Lattes - Gare Saint-Roch vélo|Deux Ponts - Gare Saint-Roch vélo|Providence - Ovalie vélo|Pérols Etang de l'Or vélo|Albert 1er - Cathédrale vélo|Saint-Guilhem - Courreau vélo|Sud De France vélo

### **Carte de température**
![](https://raw.githubusercontent.com/ElouanFiore/SAE15_BRUALLA_FIORE/main/heatmap.png)
Ce graphique représente l'indice de corrélation pour chaque parkings voitures par rapport aux parkings vélos. On peut constater que certains parkingis n'ont aucune corrélation, comme FR_MTP_POLY, bien qu'il soit ouvert les données n'ont pas bougés lors de la capture [(données)](https://raw.githubusercontent.com/ElouanFiore/SAE15_BRUALLA_FIORE/main/databrutes/FR_MTP_POLY.csv), les capteurs de présence pour ce parking sont donc considérés comme déféctueux. C'est la même chose pour [FR_MTP_ARCE](https://raw.githubusercontent.com/ElouanFiore/SAE15_BRUALLA_FIORE/main/databrutes/FR_MTP_ARCE.csv), [FR_MTP_CIRC](https://raw.githubusercontent.com/ElouanFiore/SAE15_BRUALLA_FIORE/main/databrutes/FR_MTP_CIRC.csv) et le parking vélo [034](https://raw.githubusercontent.com/ElouanFiore/SAE15_BRUALLA_FIORE/main/databrutes/034.csv).

### **Les plus corrélés**
![](https://raw.githubusercontent.com/ElouanFiore/SAE15_BRUALLA_FIORE/main/graph.png)

Ce graphique montre le parking voiture Mosson et le parking vélo Renouvier, ils ont le facteur de corrélation le plus proche de 1. Ces parkings ne sont pas proches géographiquement, ça peut donc être dû à une coincidence. Mais le parking Mosson se trouve en périphérie de Montpellier, on peut donc imaginer que s'il y a une ligne de tramway présente les usagés l'emprunteront pour se rendre au parking Renouvier situé plus à l'interieur de Montpellier pour prendre un vélo.

### **Données totales**
Avec le compte rendu du total des parkings, nous pouvons voir que le nombre de places libres est suffisant avec plus de 50% de places libre en moyenne sur Montpellier. Et le service de vélos de Montpellier est efficace, le pourcentage de vélos diponibles est en moyenne de 36% mais c'est un chiffre à surveiller car cet été le nombre de vélos empruntés devrait être plus important. Enfin la transition voiture/vélo est efficace, même en hiver on obtient des facteurs de corrélations intéressant sur les parkings voitures/vélos.
