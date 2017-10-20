from random import shuffle, random, randint
from sys import argv
from time import clock
import matplotlib.pyplot as plt
import os    
    

def lecture(filename, separator) :
    fichier = open(filename,"r")
    Matrix = []
    cpt = 0

    for i in fichier:
        if(separator == None) :
            ligne = i.split()
        else : 
            ligne = i.split(separator)
        ligne[len(ligne)-1] = ligne[len(ligne)-1].rstrip('\n')
        
        for j in range(len(ligne)) :
            ligne[j] = int(ligne[j])
        
        Matrix.append(ligne)
        cpt += 1

    fichier.close()
    print(cpt,"lignes lues dans le fichier",filename)
    return Matrix


# Lit le fichier des résultats pour ensuite l'afficher
def readResults() :
	fichier = open("resultats.csv", "r")
	results = []
	first = True

	for i in fichier :
		ligne= i.split(",")
		ligne[len(ligne)-1] = ligne[len(ligne)-1].rstrip('\n')

		for j in range(0, len(ligne)) :
			ligne[j] = float(ligne[j])

		if(first) :
			results.append([ligne[0]])
			results.append([ligne[1]])
			first = False
		else :
			results[0].append(ligne[0])
			results[1].append(ligne[1])
	fichier.close()
	return results


# Affiche les résultats sur deux graphes, un avec le cout min et l'autre avec le cout moyen
def printResults(results) :
	fig, ax1 = plt.subplots()
	ax1.plot(results[0], "-k")
	txt = str(results[0][len(results[0])-1])
	ax1.text(len(results[0]), results[0][len(results[0])-1], txt)
	ax1.plot(results[1], "-r")
	txt = str(results[1][len(results[1])-1])
	ax1.text(len(results[1]), results[1][len(results[1])-1], txt)
	plt.show()
	plt.pause(1)


# Permet de calculer le cout total de la liste <path> 
def calculCout(matrix, path) :
    coutDelta = 0
    for i in range(len(path)-1) :
        coutDelta += matrix[path[i]][path[i+1]]
    return coutDelta


# Renvoi une liste avec les couts de chaque sous liste
def listOfCosts(matrix, paths) :
	listRes = []
	for i in range(len(paths)) :
		listRes.append(calculCout(matrix, paths[i]))
	return listRes


def createPopulation(lenMatrix, nPop) :
    pathMatrix = []
    print("Creating population")
    for i in range(0, nPop) :
        path = list(range(1, lenMatrix))
        shuffle(path)
        path.append(0);
        path = [0] + path
        pathMatrix.append(path);
    return pathMatrix
        

# Fais la mutation du chromosome
# Pour chaque gene, si random > pMutate
# Switch avec le prochain à muter, au final ca fait une boucle
def mutate(path, pMutate) :
    toBeMutated = []
    for i in range(1, len(path)-1) :
        if(random() < pMutate) : 
            toBeMutated.append(i)
    if(len(toBeMutated) >= 2) :
        tmp = path[toBeMutated[0]]
        for i in range(0, len(toBeMutated)-1) :
            path[toBeMutated[i]] = path[toBeMutated[i+1]]
        path[toBeMutated[len(toBeMutated)-1]] = tmp
    

# Crossover
def crossOver(path1, path2) :
    iCrossover = int(random() * (len(path1)-1))
    iChild = iCrossover
    iP2 = 1
    child = path1[0:iCrossover]
    while(iChild < len(path1)-1) :
    	if(path2[iChild] not in child) : 
    		child.append(path2[iChild])
    	else :
    		while(path2[iP2] in child) :
    			iP2 += 1
    		child.append(path2[iP2])
    	iChild += 1
    child.append(0)
    return child


# Renvoi l'indice de la valeur maximum de la liste
def getIndexMaxCost(listInt) :
	iMax = 0
	for i in range(1, len(listInt)) :
		if(listInt[i] >= listInt[iMax]) :
			iMax = i
	return iMax


# Renvoi renvoi le cout minimal de la liste d'individus
def getMinimalCost(matrix, paths) :
	minCost = calculCout(matrix, paths[0])
	iMin = 0
	for i in range(1, len(paths)) :
		tmpCost = calculCout(matrix, paths[i])
		if(tmpCost <= minCost) :
			minCost = tmpCost
			iMin = i
	return iMin,minCost


# Renvoi renvoi le cout moyen de la liste d'individus
def getMeanCost(matrix, paths) :
	meanCost = 0
	for i in range(len(paths)) :
		meanCost += calculCout(matrix, paths[i])
	return meanCost/len(paths)


# Affiche la matrix
def printMatrix(matrix, paths) :
	for i in range(0,len(paths)) :
		print(paths[i], calculCout(matrix, paths[i]))


def genetique(filename, separator, nPop, pMutate) :
	matrix = lecture(filename, separator)
	parentPop = createPopulation(len(matrix), nPop)
	bufferCosts = list(range(0,11))
	cptGen = 0

	start = clock()

	fichier = open("resultats.csv", "w")

	print("Starts evolving")
	print("Gen.\tMin\tDetails\tMean")
	print("----\t---\t-------\t----")
	print("Press Enter ...")
	input()
	# Pour savoir si on a finis on regarde 10 générations en arrière si le cout du meilleur est toujours le même
	while(bufferCosts[(cptGen-10)%11] != bufferCosts[cptGen%11]) : 
		# os.system('cls' if os.name == 'nt' else 'clear')
		cptGen += 1
		# Création de la population enfant
		childPop = []
		for i in range(0,nPop) :
			p1 = randint(0,nPop-1)
			p2 = randint(0,nPop-1)
			while(p1 == p2) :
				p1 = randint(0,nPop-1)
				p2 = randint(0,nPop-1)
			child = crossOver(parentPop[p1], parentPop[p2])
			mutate(child, pMutate)
			childPop.append(child)

		# Sélection des nPop meilleurs individus
		parentPop.extend(childPop) # On rassemble les parents et enfants
		listCost = listOfCosts(matrix, parentPop) # On crée une liste avec les couts de chaque individu
		while(len(parentPop) > nPop) : # On supprime un à un les nPop plus grands couts, il ne restera que les meilleurs individus
			iMax = getIndexMaxCost(listCost)
			parentPop.pop(iMax)
			listCost.pop(iMax)
		bufferCosts[cptGen%11] = getMeanCost(matrix,parentPop)

		iMin, cMin = getMinimalCost(matrix, parentPop)
		print(cptGen,cMin,parentPop[iMin],round(bufferCosts[cptGen%11],5))
		fichier.write("%d,%d\n" % (cMin,round(bufferCosts[cptGen%11],5)))
	fichier.close()

	stop = clock()
	print("Temps exécution :",stop-start)

	results = readResults()
	printResults(results)


try :
	filename   = argv[1]
	separator  = argv[2]
	nPop       = int(argv[3])
	pMutate    = float(argv[4])
except IndexError :
	print("Not enough arguments")
	print("needed : <filename> <separator or None> <nPop> <pMutate>")
	exit()

if(separator == "None") :
	separator = None

genetique(filename, separator, nPop, pMutate)