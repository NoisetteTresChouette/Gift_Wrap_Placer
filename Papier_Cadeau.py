import numpy as np
from time import time
from random import randint
import matplotlib.pyplot as plt

def tri(cadeaux):# je tri dans l'ordre décroissant des plus grands plus long côtés, puis des plus grands plus courts côtés.
    cadeaux_tries = []
    cadeaux_verifies = [0 for k in range(len(cadeaux))]# cette liste indique les rectangles déjà triés
    for _ in range(len(cadeaux)):
        l_max = 0
        L_max = 0
        i =0
        while cadeaux_verifies[i] != 0:#je cherche le premier cadeau qui n'est pas trié
            i += 1
        index_max = i
        for i in range(len(cadeaux)):
            if cadeaux_verifies[i] == 0:
                if max(dim(cadeaux[i])) > L_max:
                    index_max = i
                    L_max,l_max = max(dim(cadeaux[i])),min(dim(cadeaux[i]))
                elif max(dim(cadeaux[i])) == L_max:
                    if min(dim(cadeaux[i])) > l_max:
                        index_max = i
                        L_max,l_max = max(dim(cadeaux[i])),min(dim(cadeaux[i]))
        cadeaux_verifies[index_max] = 1
        cadeaux_tries.append([l_max,L_max, index_max] )
    return cadeaux_tries# je revoie avec les longueurs des côtés l'indice du cadeau correspondant, car nous devons renvoier avec la fonction papier_minimal une liste dans le même ordre que la liste 'cadeaux' innitialle

def dim(cadeau):# renvoie la dimension du rectangle de papier cadeau pour un cadeau de dimension 'cadeau'
    return 2*(cadeau[0]+cadeau[1])+2 , cadeau[1]+cadeau[2]+2

def papier_minimal(cadeaux):
    cadeaux_tries = tri(cadeaux)
    cadeaux_retour = [0 for i in range(len(cadeaux)) ]# le '0' est arbitraire, je charche seulement à distinguer les cadeaux déjà placés et ceux qui ne le sont pas encore
    L_tot,l_tot = cadeaux_tries[0][1],cadeaux_tries[0][0]# dimension du grand rectangle contenant tous les rectangles déjà posés
    cadeaux_retour[cadeaux_tries[0][2]] = cadeaux[cadeaux_tries[0][2]] + [0,0,l_tot,L_tot]# je place le plus grand cadeau verticalement, en [0,0], d'où les valeurs innitialles de L_tot et l_tot.
    #   L_tot >= l_tot innitialement, le plus grand rectangle étant placé verticalement
    pts_occupes = set()# je garde dans cet ensemble l'ensemble des points contenus dans un rectangle déjà placé. ATTENTION: ceci n'inclut pas les frontières. L'utilisation d'un ensemble permet de faire des tests d'appartenance de complexité élémentaire
    for x in range(l_tot):# je rajoute donc ici l'ensemble des point du premier rectangle
        for y in range(L_tot):
            pts_occupes.add((x,y))
    for i in range(1,len(cadeaux_tries)):# je cherche la position des cadeaux dans l'ordre décroissant
        insertion  = False# cette varialbe est à True si le nouveau rectangle peut être placé dans le grand rectangle L_tot,l_tot, sans superposition. Je l'initialise ici à False
        A = np.inf# aire que nous chercons à minimiser
        l,L = tuple(cadeaux_tries[i][0:2])# petit et grand côté du nouveau rectangle
        for x in range(l_tot):
            for y in range(L_tot):
                if (x,y) not in pts_occupes:# je parcours l'ensemble des points du grand rectangle (L_tot,l_tot) qui ne sont pas déjà inclus dans un rectangle.
                    if superposition(cadeaux_retour,[x,y,x+l,y+L]) == False:# on vérifie si il y a superposition en plaçant le nouveau cadeau verticalement aux coordonnées (x,y)
                        insertion = True# si il existe une coordonnée sans superposition, alors le nouveau rectangle peut être placé dans le grand rectangle
                        if max(l_tot,x+l) * max(L_tot,y+L) < A:# je regarde si nous avons trouvé une plus petite aire en ces coordonnées
                            A = max(l_tot,x+l) * max(L_tot,y+L)
                            candidat = cadeaux[cadeaux_tries[i][2]] + [x,y,x+l,y+L]# je retiens celle-ci si c'est le cas
                    if superposition(cadeaux_retour,[x,y,x+L,y+l]) == False:# identiquement mais à l'horizontal
                        insertion = True
                        if max(l_tot,x+L) * max(L_tot, y+l) < A:
                            A = max(l_tot,x+L) * max(L_tot, y+l)
                            candidat = cadeaux[cadeaux_tries[i][2]] + [x,y,x+L,y+l]
                    # L'utilisation de l'ensemble 'pts_occupés' permet donc d'éviter un grand nombre d'appels de la fonction 'superposition'. Cela permet donc d'économiser beaucoup de temps.
        if insertion == False:# si je n'ai pas pu placer le nouveau rectangle dans le grand rectangle, je charche alors à minimiser l'aire en le plaçant à côté du rectangle.
            if (L_tot + L) * max(l_tot, l) < A:# en le plaçant à la verticale en coorodonnées y supérieure
                A = (L_tot + L) * max(l_tot, l)
                candidat = cadeaux[cadeaux_tries[i][2]] + [0,L_tot,l,L_tot+L]
            if (L_tot + l) * max(l_tot, L) < A:# à l'horizontale
                A = (L_tot + l) * max(l_tot, L)
                candidat = cadeaux[cadeaux_tries[i][2]] + [0,L_tot,L,L_tot+l]
            if (l_tot + L) * max(L_tot, l) < A:# en le plaçant à l'horizontale en coorodonnées x supérieure
                A = (l_tot + L) * max(L_tot, l)
                candidat = cadeaux[cadeaux_tries[i][2]] + [l_tot,0,l_tot+L,l]
            if (l_tot + l) * max(L_tot, L) < A:# à la verticale
                A = (l_tot + l) * max(L_tot, L)
                candidat = cadeaux[cadeaux_tries[i][2]] + [l_tot,0,l_tot+l,L]
        for new_x in range(candidat[3],candidat[5]):
            for new_y in range(candidat[4],candidat[6]):
                pts_occupes.add((new_x,new_y))# je mets à jour l'ensemble 'pts_occupes'
        cadeaux_retour[cadeaux_tries[i][2]] = candidat[:]# je mets à jour 'cadeaux_retour'
        L_tot = max(L_tot,cadeaux_retour[cadeaux_tries[i][2]][6])# je mets à jour 'L_tot'
        l_tot = max(l_tot, cadeaux_retour[cadeaux_tries[i][2]][5])# je mets à jour 'l_tot'
    return cadeaux_retour

def superposition(cadeaux_retour,coords):# Je vérifie si le rectangle de coordonnées [x1,y1,x2,y2] = coords se superpose ou non avec les ractangles déjà positionnés
    for c in cadeaux_retour:
        if c != 0:# les cas où c!=0 correspondent aux cadeaux placés
            if (c[3] <= coords[0] < c[5]) and ((c[4] <= coords[1] < c[6]) or (c[4] < coords[3] <= c[6]) or (coords[1] <= c[4] < coords[3])):
                return True#    je renvoie True si il y a superposition
            elif (c[3] < coords[2] <= c[5]) and ((c[4] <= coords[1] < c[6]) or (c[4] < coords[3] <= c[6]) or (coords[1] <= c[4] < coords[3])):
                return True
            elif (coords[0] <= c[3] < coords[2]) and ((coords[1] <= c[4] < coords[3]) or (coords[1] < c[6] <= coords[3]) or (c[4] <= coords[1] < c[6])):
                return True
    return False

# différentes foctions tests qui m'ont permisent de vérifier mon programme, et d'évaluer l'efficacité et la rapidité d'exécution. PS: c'est pas beau je ne me suis pas trop attardé dessus.

def test_show(nbr,taille=10):# j'affiche la disposition des cadeaux trouvés par mon algorithme, pour le une liste de 'nbr' cadeaux' de dimensions entre 1 et 'taille'
    cadeaux = [[randint(1,taille+1),randint(1,taille+1),randint(1,taille+1)] for k in range(0,nbr)]
    start = time()
    print("début")
    cadeaux_retour = papier_minimal(cadeaux)
    print('fini: '+str(time()-start))# je chronomètre la durée d'exécution duu programme
    x_min = min([cadeaux_retour[k][3] for k in range(len(cadeaux_retour))])
    x_max = max([cadeaux_retour[k][5] for k in range(len(cadeaux_retour))])
    y_min = min([cadeaux_retour[k][4] for k in range(len(cadeaux_retour))])
    y_max = max([cadeaux_retour[k][6] for k in range(len(cadeaux_retour))])
    aire = (x_max-x_min) * (y_max-y_min)# je mesure l'aire

    print("\nListe:\n"+str(cadeaux_retour) +"\n\nAire:\n"+str(aire))# je print le résultat
    colors = [[0 for j in range(x_min,x_max)] for i in range(y_min,y_max) ]
    M = [[[1.0,1.0,1.0] for j in range(x_min,x_max)] for i in range(y_min,y_max) ]
    for i in range(y_min,y_max):
        for j in range(x_min,x_max):
            for c in cadeaux_retour:
                if (c[3] <= j < c[5]) and  (c[4] <= i < c[6]):
                    colors[i-y_min][j-x_min] += 1
            if colors [i-y_min][j-x_min] >1:
                M[i-y_min][j-x_min] = [1.0,0.0,0.0]# j'ai colorie en rouge les zones où il y a plus d'un rectangle
            elif colors [i-y_min][j-x_min] == 1:
                M[i-y_min][j-x_min] = [0.0,1.0,0.0]# et en vert où il n'y a qu'un seul rectangle
    # je calcul après l'efficacité du programme, càd la proportion en surface de l'ensemble des rectangles, par rapport à la surface du grand rectangle
    surface = 0
    x_min = cadeaux_retour[0][3]
    x_max = cadeaux_retour[0][5]
    y_min = cadeaux_retour[0][4]
    y_max = cadeaux_retour[0][6]
    for c in cadeaux_retour:
        x,y = dim(c[:3])
        surface += x*y
        if x_min > c[3]:
            x_min = c[3]
        if y_min > c[4]:
            y_min = c[4]
        if x_max < c[5]:
            x_max = c[5]
        if y_max < c[6]:
            y_max = c[6]
    eff = (surface/((x_max-x_min)*(y_max-y_min)))
    print(eff)
    plt.imshow(M)
    plt.show()# j'affiche la disposition des cadeaux

def test_eff(nbr,taille=10):# je calcul l'efficacité du programme en fonction du nombre de cadeaux (somme des surfaces de tous les rectangles / surface du grand rectangle)
    cadeaux = [[randint(1,taille+1),randint(1,taille+1),randint(1,taille+1)] for k in range(0,nbr)]
    start = time()
    print('début')
    cadeaux_retour = papier_minimal(cadeaux)
    end=time()
    print('Fini:\n'+str(end-start))
    surface = 0
    x_min = cadeaux_retour[0][3]
    x_max = cadeaux_retour[0][5]
    y_min = cadeaux_retour[0][4]
    y_max = cadeaux_retour[0][6]
    for c in cadeaux_retour:
        x,y = dim(c[:3])
        surface += x*y
        if x_min > c[3]:
            x_min = c[3]
        if y_min > c[4]:
            y_min = c[4]
        if x_max < c[5]:
            x_max = c[5]
        if y_max < c[6]:
            y_max = c[6]
    eff = (surface/((x_max-x_min)*(y_max-y_min)))
    print('\nEfficacité:'+ str(eff))
    return eff,end-start

def test_moy(nbr,taille=10,effectif=20):# je calcule la moyenne temporelle et d'efficacité du programme pour un nombre 'effectif' de listes composées de 'nbr' cadeaux de taille entre 1 et 'taille'
    somme_efficacité = 0
    somme_temps = 0
    for i in range(effectif):
        efficacité,temps = test_eff(nbr,taille)
        somme_efficacité += efficacité
        somme_temps += temps
    return somme_temps/effectif, somme_efficacité/effectif
""" après avoir effectué une moyenne sur 200 listes de 100 cadeaux de taille entre 1 et 10, j'ai obtenu en moyenne un temps de 20.45 secones pour une efficacité moyenne de 0.9288

ces fonctions de tests m'ont permis notamment de vérifier l'utilitié de la variable 'insertion'. En effet, sans insertion, les moyennes de temps et d'efficacité sont un peu près similaire, cependant la grande différence réside dans les cas critiques (les tests sont effectués sur les listes de 100 cadeaux).
En effet, il y a certain cas où, sans 'insertion', l'algorithme pouvait prendre de 70 jusqu'à 100 secondes, et l'efficacité tombé alors autour des 0,70 0,80. Tandis qu'avec 'insertion', les pires cas se situent autour des 40 secondes, avec des efficacités proche des 90%."""
