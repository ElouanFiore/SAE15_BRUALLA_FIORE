# -*- coding: utf-8 -*-
from math import sqrt

### Ce fichier python servira à epauler notre fichier de recupération ###

# Fonction qui calcule la moyenne et qui la renvoie arrondi à 2 décimales près #

def moyenne(L):
	moy=0
	for x in L:
		moy+=int(x)
	moy=moy/len(L)
	return round(moy,2)

# Fonction qui calcule l'écart-type et qui la renvoie arrondie à 2 décimales près #

def ecart_type(L):
	moy=moyenne(L)
	ecart=0
	for x in L:
		ecart+=(int(x)-moy)**2
	ecart=sqrt(ecart/len(L))
	return round(ecart,2)

# Fonction qui calcule la covariance et qui la renvoie arrondie à 2 décimales près #

def covar(x,y):
	moyX=moyenne(x)
	moyY=moyenne(y)
	result=0
	for index,val in enumerate(x):
		result+=(int(val)-moyX)*(int(y[index])-moyY)
	return round(result/len(x),2)

# Fonction qui calcule le pourcentage et qui le renvoie arrondi à  2 décimales près #

def pourcentage(a,b):
	return round(int(a)*100/int(b),2)
