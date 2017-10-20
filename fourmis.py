from random import shuffle, random, randint
from sys import argv, maxsize
import os   
import time
import matplotlib.pyplot as plt
    

# Lit le fichier contenant les distances entre les  de villes
def readDistances(filename, separator) :
    fichier = open(filename,"r")
    Matrix = []
    cpt = 0

    for i in fichier:
        if(separator == None) :
            ligne = i.split()
        else : 
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


# Lit le fichier contenant les coordonnées de villes (Non utilisé)
def readCoordonates(filename, separator) :
    fichier = open(filename,"r")
    coord = []
    cpt = 0

    for i in fichier:
        if(separator == None) :
            ligne = i.split()
        else : 
            ligne = i.split(separator)
        ligne[len(ligne)-1] = ligne[len(ligne)-1].rstrip('\n')
        
        for j in range(0,len(ligne)) :
            ligne[j] = int(ligne[j])
        
        coord.append(ligne)
        cpt += 1

    fichier.close()
    print(cpt,"lignes lues dans le fichier",filename)
    return coord


# Affiche la matrix
def printMatrix(paths) :
    for i in range(len(paths)) :
        print(i,paths[i])

# Affiche la matrice de pheromons (flottanss arrondis)
def printPhero(pheromons) :
    for i in range(len(pheromons)) :
        print("[",end = " ") 
        for j in range(len(pheromons[i])) :
            print(round(pheromons[i][j],2),end = " ")
        print("]")


# Affiche les chemins des fourmis sur un graphe
def printGraphPaths(pathsAnt) :
    ax = range(0,len(pathsAnt[0]))
    plt.clf()
    for i in range(len(pathsAnt)) :
        plt.plot(pathsAnt[i],ax,":k")
    plt.show()
    plt.pause(0.1)


# Permet de calculer le cout total de la liste <path> 
def calculCout(matrix, path) :
    coutDelta = 0
    for i in range(len(path)-1) :
        coutDelta += matrix[path[i]][path[i+1]]
    return coutDelta


# Permet de calculer le cout moyen entre chaque ville 
def calculMeanCost(matrix) :
    mean = 0
    sizeMat = 0
    for i in range(len(matrix)) :
        for j in range(len(matrix[i])) :
            if(i!=j):
                mean += matrix[i][j]
                sizeMat += 1
    return mean / sizeMat


# Renvoi renvoi le cout minimum et moyen de la liste d'individus
def getInfosCost(matrix, paths) :
    meanCost = 0
    minCost = maxsize
    iMin = -1
    for i in range(len(paths)) :
        tmpCost = calculCout(matrix, paths[i])
        meanCost += tmpCost
        if(tmpCost <= minCost) :
            minCost = tmpCost
            iMin = i
    return iMin, minCost, meanCost/len(paths)


# Renvoi la moyenne de pheromons par arrete
def getMeanPhero(pheromons) :
    mean = 0 
    sizeMat = 0
    for i in range(len(pheromons)) :
        for j in range(len(pheromons[i])) :
            mean += pheromons[i][j]
        sizeMat += len(pheromons[i])
    return mean/sizeMat


# Initialise la matrice avec que des 1 (pour les pheromons)
def initMatrix(matrix, taille) : 
    for i in range(0, taille) :
        matrix.append([1] * taille)


# Calcul de la probabilité pour se déplacer de ville
def pTransi(matrix, pheromons, currCity, nextCity, villesNonVisitees, alpha, beta) : 
    somme = 0
    for i in range(len(villesNonVisitees)) :
        somme += (pheromons[currCity][villesNonVisitees[i]] ** alpha) * (( 1 / matrix[currCity][villesNonVisitees[i]]) ** beta)

    # Probabilité pour aller au prochain sommet 
    pTransi = ((pheromons[currCity][nextCity] ** alpha) * (( 1 / matrix[currCity][nextCity]) ** beta)) / ( somme )
    return pTransi


# Ajoute les pheromons sur le chemin parcouru par la fourmis
def antDropPheromon(matrix, villesVisitees, pheromonsResults, qConst) :
    for i in range(len(villesVisitees)-1) :
        pheromonsResults[villesVisitees[i]][villesVisitees[i+1]] += (qConst / calculCout(matrix, villesVisitees))


# Fais s'évaporer les pheromons selon le parametre rho
def evapPheromon(pheromons, pheromonsResults, rho) :
    for i in range(len(pheromons)) :
        for j in range(len(pheromons)) :
            pheromonsResults[i][j] = pheromons[i][j] * (1-rho) 

        
# Deplacement des fourmis
def antFindPath(iFourmis, matrix, pheromons, alpha, beta) : 
    currCity = iFourmis
    villesNonVisitees = list(range(len(matrix)))
    villesNonVisitees.remove(currCity)
    villesVisitees = [currCity]   

    # len(matrix) villes à parcourir
    for i in range(len(matrix)-1) :
        pMax = 0
        # Trouve le P le plus grand pour se déplacer d'une ville
        for j in range(len(villesNonVisitees)) :
            pTmp = pTransi(matrix, pheromons, villesVisitees[-1], villesNonVisitees[j], villesNonVisitees, alpha, beta)
            if(pTmp > pMax) :  
                pMax = pTmp
                indiceNextVille = villesNonVisitees[j]
        # On ajoute la ville visitée dans la liste et on retire de non visitée
        villesVisitees.append(indiceNextVille)
        villesNonVisitees.remove(indiceNextVille)
    return villesVisitees


# Applique la méthode des colonies de fourmis
def fourmis(filename, separator, nMax, alpha, beta, rho, qConst) :

    # Lecture du fichier et création des matrices
    matrix = readDistances(filename, separator)
    if(qConst == 0) :
        qConst = 2*calculMeanCost(matrix)
    print("qConst =",qConst)
    
    start = time.clock()

    pheromons        = []
    pheromonsResults = []
    
    cptAllSamePath = 0

    cptGen = 1

    fichier = open("resultats.csv", "w")

    # Initialisation matrices
    initMatrix(pheromons, len(matrix))
    initMatrix(pheromonsResults, len(matrix))

    #Boucle des itérations
    while(cptGen < nMax) :
        pathsAnt = []
        cptAllSamePath = 0

        # Evaporation des pheromones
        evapPheromon(pheromons, pheromonsResults, rho)
        
        # Deplacement des fourmis
        for i in range(len(matrix)) :
            pathAnt = antFindPath(i, matrix, pheromons, alpha, beta)
            antDropPheromon(matrix, pathAnt, pheromonsResults, qConst)
            pathsAnt.append(pathAnt)
        pheromons = pheromonsResults 
        iMin,cMin,cMean  = getInfosCost(matrix,pathsAnt)
        print("Gen.",cptGen," \tMin:",iMin,cMin," \tMean:",round(cMean,3)," \tMeanPhero:",round(getMeanPhero(pheromons),5))
        fichier.write("%d,%d\n" % (cMin,cMean))
        cptGen += 1
    fichier.close()

    stop = time.clock()
    print(pathsAnt[iMin])
    print("Temps exécution :",stop-start)

    results = readResults()
    printResults(results)


# Récupération des paramètres du programme et appel de la fonction principale
try :
    filename   = argv[1]
    separator  = argv[2]
    nMax       = int(argv[3])
    alpha      = float(argv[4])
    beta       = float(argv[5])
    rho        = float(argv[6])
    if(len(argv) > 7) :
        qConst = float(argv[7])
    else : 
        qConst = 0
except IndexError :
    print("Not enough arguments")
    print("Needed : <filename> <separator or 'None'> <nb iterations> <alpha> <beta> <rho> [optional <Q>]")
    exit()

if(separator == "None") :
    separator = None

fourmis(filename, separator, nMax, alpha, beta, rho, qConst)