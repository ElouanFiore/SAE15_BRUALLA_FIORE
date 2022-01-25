from math import sqrt


def moyenne(L):
	moy=0
	for x in range(len(L)):
		moy=L[x]+moy
	moy=moy/len(L)
	return round(moy,2)

def ecart_type(L):
	moy=moyenne(L)
	ecart=0
	for x in range(len(L)):
		ecart=ecart+(L[x]-moy)**2
	ecart=sqrt(ecart/len(L))
	return(ecart)

def covar(x,y):
	moyX=moyenne(x)
	moyY=moyenne(y)
	result=0
	for index,val in enumerate(x):
		result+=(val-moyX)*(y[index]-moyY)
	return result/len(x)