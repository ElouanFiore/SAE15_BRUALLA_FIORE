from math import sqrt

def moyenne(L):
    return sum(L)/len(L)

def sigma(L, moyenne):
    somme = 0
    for i in L:
        somme += (i - moyenne)**2
    return sqrt(somme/len(L))

def pourcentage(a, b):
	return (a/b)*100
