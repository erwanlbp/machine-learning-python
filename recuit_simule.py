from random import random, randint
from math import exp, fabs
from time import clock
import matplotlib.pyplot as plt
from sys import maxsize, argv


# Lit le fichier et retourne une matrice 2D d'entiers 
def lecture(filename, separator) :
	fichier = open(filename,"r")
	Matrix = []
	cpt = 0

	for i in fichier:
		ligne = i.split(separator)
		ligne[len(ligne)-1] = ligne[len(ligne)-1].rstrip('\n')
		
		for j in range(0,len(ligne)) :
			ligne[j] = int(ligne[j])
		
		Matrix.append(ligne)
		cpt += 1

	fichier.close()
	print(cpt,"lignes lues dans le fichier",filename)
	return Matrix


# Lit le fichier des résultats pour ensuite l'afficher
def lectureResultats() :
	fichier = open("resultats.csv", "r")
	results = []
	first = True

	for i in fichier :
		ligne= i.split(",")
		ligne[len(ligne)-1] = ligne[len(ligne)-1].rstrip('\n')

		for j in range(0, len(ligne)) :
			ligne[j] = int(ligne[j])

		if(first) :
			results.append([ligne[0]])
			results.append([ligne[1]])
			results.append([ligne[2]])
			first = False
		else :
			results[0].append(ligne[0])
			results[1].append(ligne[1])
			results[2].append(ligne[2])
	fichier.close()
	return results


# Permet de calculer le cout total de la liste <path> 
def calculCoutDelta(matrix, path) :
	coutDelta = 0
	for i in range(0, len(path)-1) :
		coutDelta += matrix[path[i]][path[i+1]]
	return coutDelta


# Applique la transformation inversion
def inversion(matrix, path, temperature) :
	indice = randint(1, len(path)-3)
	
	lAvant = [path[indice-1], path[indice], path[indice+1], path[indice+2]]
	lApres = [path[indice-1], path[indice+1], path[indice], path[indice+2]]

	deltaAvant = calculCoutDelta(matrix, lAvant)
	deltaApres = calculCoutDelta(matrix, lApres)

	print("Inversion\t[",indice,",",indice+1,"]\t",deltaApres-deltaAvant,"\t", end=' ')
	if(deltaApres < deltaAvant or random() < exp(-deltaApres / temperature)) :
		tmp = path[indice]
		path[indice] = path[indice+1]
		path[indice+1] = tmp
		return 1, deltaApres-deltaAvant
	else :
		return 0, 0


# Applique la transformation deplacement
def deplacement(matrix, path, temperature) :
	origine = randint(1, len(path)-2)
	destination = randint(1, len(path)-2)
	while(origine == destination) :
		origine = randint(1, len(path)-2)
		destination = randint(1, len(path)-2)

	lAvantT1 = [path[origine-1], path[origine], path[origine+1]]
	lAvantT2 = [path[destination-1], path[destination]]
	lApresT1 = [path[origine-1], path[origine+1]]
	lApresT2 = [path[destination-1], path[origine], path[destination]]

	deltaAvant = calculCoutDelta(matrix, lAvantT1) + calculCoutDelta(matrix, lAvantT2)
	deltaApres = calculCoutDelta(matrix, lApresT1) + calculCoutDelta(matrix, lApresT2)
	
	print("Deplacement\t[",origine,"=>",destination,"]\t",deltaApres-deltaAvant,"\t", end=' ')
	if(deltaApres < deltaAvant or random() < exp(-deltaApres / temperature)) :
		tmp = path[origine]
		if(origine < destination) :
			destination -= 1
		path.remove(path[origine])
		path.insert(destination, tmp)
		return 1, deltaApres-deltaAvant
	else :
		return 0, 0


# Applique la transformation echange
def echange(matrix, path, temperature) :
	troncon1 = randint(1, len(path)-3)
	troncon2 = randint(1, len(path)-3)
	while(fabs(troncon1-troncon2) <= 2) :
		troncon1 = randint(1, len(path)-3)
		troncon2 = randint(1, len(path)-3)

	lAvantT1 = [path[troncon1-1], path[troncon1], path[troncon1+1], path[troncon1+2]]
	lAvantT2 = [path[troncon2-1], path[troncon2], path[troncon2+1], path[troncon2+2]]
	lApresT1 = [path[troncon1-1], path[troncon2], path[troncon2+1], path[troncon1+2]]
	lApresT2 = [path[troncon2-1], path[troncon1], path[troncon1+1], path[troncon2+2]]

	deltaAvant = calculCoutDelta(matrix, lAvantT1) + calculCoutDelta(matrix, lAvantT2)
	deltaApres = calculCoutDelta(matrix, lApresT1) + calculCoutDelta(matrix, lApresT2)

	print("Echange\t\t[",troncon1,"<=>",troncon2,"]\t",deltaApres-deltaAvant,"\t", end=' ')
	if(deltaApres < deltaAvant or random() < exp(-deltaApres / temperature)) :
		tmp1 = path[troncon1]
		tmp2 = path[troncon1+1]
		path[troncon1]   = path[troncon2]
		path[troncon1+1] = path[troncon2+1]
		path[troncon2]   = tmp1
		path[troncon2+1] = tmp2
		return 1, deltaApres-deltaAvant
	else :
		return 0, 0


# Applique la transformation croisement
def croisement(matrix, path, temperature) :
	seg1 = randint(1, len(path)-2)
	seg2 = randint(1, len(path)-2)
	while(fabs(seg1-seg2) <= 1) :
		seg1 = randint(1, len(path)-2)
		seg2 = randint(1, len(path)-2)

	lAvantT1 = [path[seg1-1], path[seg1], path[seg1+1]]
	lAvantT2 = [path[seg2-1], path[seg2], path[seg2+1]]
	lApresT1 = [path[seg1-1], path[seg2], path[seg1+1]]
	lApresT2 = [path[seg2-1], path[seg1], path[seg2+1]]

	deltaAvant = calculCoutDelta(matrix, lAvantT1) + calculCoutDelta(matrix, lAvantT2)
	deltaApres = calculCoutDelta(matrix, lApresT1) + calculCoutDelta(matrix, lApresT2)

	print("Croisement\t[",seg1,"<=>",seg2,"]\t",deltaApres-deltaAvant,"\t", end=' ')
	if(deltaApres < deltaAvant or random() < exp(-deltaApres / temperature)) :
		tmp = path[seg1]
		path[seg1]   = path[seg2]
		path[seg2]   = tmp
		return 1, deltaApres-deltaAvant
	else :
		return 0, 0


# Affiche les résultats sur deux graphes, un avec le cout delta et l'autre avec la temperature
def afficherResults(results) :
	plt.figure(1)
	plt.title("Résultats")
	plt.subplot(211)
	plt.title("Cout delta")
	plt.plot(results[1], ",k")
	plt.subplot(212)
	plt.title("Temperature")
	plt.plot(results[2], ",r")
	plt.show()
	plt.pause(1)
	input()


# Fonction principale appliquant le recuit simulé
def recuit_simule(filename, separator, temperature, step, limit) :
	matrix = lecture(filename, separator)

	if(len(matrix) < 5) :
		print("Il doit y avoir au moins 5 villes sinon cet algorithme ne fonctionnera pas")
		exit()

	plt.ion()
	start = clock()

	#Creation du chemin resultat
	path = list(range(0, len(matrix)))
	path.append(0)
	print("Chemin initial :")
	print(path)

	#Calcul du cout du chemin
	coutDelta = calculCoutDelta(matrix,path)
	print("Le cout Delta initial est de",coutDelta,"\n")

	fichier = open("resultats.csv", "w")
	fichier.write("0,%d,%d\n" % (coutDelta,temperature))

	tx = 1
	maxCout = 0
	minCout = maxsize
	print("Transformation\tDetails\t\tDelta\tResultat\tCoutChemin, Temperature")
	print("--------------\t-------\t\t-----\t--------\t-----------------------")
	print("Press Enter ...")
	input()
	while(temperature > limit) :
		choix = randint(1, 4)
		if(choix == 1) :
			accepte, chgmtCout = echange(matrix, path, temperature)
		elif(choix == 2) : 
			accepte, chgmtCout = deplacement(matrix, path, temperature)
		elif(choix == 3) : 
			accepte, chgmtCout = inversion(matrix, path, temperature)
		elif(choix == 4) :
			accepte, chgmtCout = croisement(matrix, path, temperature)

		if(accepte > 0) :
			coutDelta += chgmtCout
			print("Accepte\t[",coutDelta,",",temperature,"]")
			if(coutDelta > maxCout) :
				maxCout = coutDelta
			if(coutDelta < minCout) :
				minCout = coutDelta

			fichier.write("%d,%d,%d\n" % (choix,coutDelta,temperature))
		else :
			print("Rejetee\t[",coutDelta,",",temperature,"]")
			temperature -= step
		tx += 1
	fichier.close()

	print("Le cout Delta calculé est de\t",calculCoutDelta(matrix,path))

	results = lectureResultats()
	afficherResults(results)

	print("Chemin final au bout de",tx,"iterations")
	print(path)

	stop = clock()
	print("Temps exécution :",stop-start)

    
try :
	filename    = argv[1]
	separator   = argv[2]
	temperature = float(argv[3])
	step        = float(argv[4])
	limit       = float(argv[5])
except IndexError :
    print("Not enough arguments")
    print("needed : <filename> <separator or None> <temperature> <step> <limit>")
    exit()

if(separator == "None") :
    separator = None

# Appel de la fonction principale
recuit_simule(filename, separator, temperature, step, limit)