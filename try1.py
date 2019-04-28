# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 13:31:51 2019

@author: mmaaz
"""

from itertools import permutations
import random as rand
import matplotlib.pyplot as plt




cityDict ={'A': [('B', 8), ('C',10), ('D', 3), ('E', 4), ('F',6)],
        'B': [('A', 8), ('C',9), ('D', 5), ('E', 5), ('F',12)],
        'C': [('A', 10), ('B',9), ('D', 7), ('E', 6), ('F',2)],
        'D': [('A', 3), ('B',5), ('C', 7), ('E', 8), ('F',11)],
        'E': [('A', 4), ('B',8), ('C', 6), ('D', 8), ('F',8)],
        'F': [('A', 6), ('B',12), ('C', 2), ('D', 11), ('E',8)]}


def main():
    permut=rand.sample(list(permutations('ABDEF')), 10)
    best=[]
    average=[]
    for i in range(100):
        initialTourCost= fitnessFunction(permut)
        parents=parentSelection(initialTourCost)
        crossed= crossOver(parents)
        mut=insertMutations(crossed)
        tenBest= survivalSelection(mut, parents)
        best.append(bestSoFar(tenBest))
        average(averageBest(tenBest))
       
        permut=removeC(tenBest)
    print(best)
    print(average)

def fitnessFunction(candidates):
    tourCost= []
    for individual in candidates:
        sumd=0;
        for i in range(len(individual)-1):
            #search i, i+1 in dcit
            for j in range(len(cityDict[individual[i]])):
                if(cityDict[individual[i]][j][0]==individual[i+1]):
                    sumd+=cityDict[individual[i]][j][1]
        
        tourCost.append((list(individual),sumd))
    #print(scores)
    return tourCost

def parentSelection(tourCost):
    aux= tourCost[:]
    parents= []
    p1= rand.sample(aux, 2)
    if(p1[0][1]> p1[1][1]):
        parents.append(p1[0])
        aux.remove(p1[0])
    else:
        parents.append(p1[1])
        aux.remove(p1[1])
    
    p2=rand.sample(aux,2)
    if(p2[0][1]> p2[1][1]):
        parents.append(p2[0])
        aux.remove(p2[0])
    else:
        parents.append(p2[1])
        aux.remove(p2[1])
    p3=rand.sample(aux,2)
    if(p3[0][1]> p3[1][1]):
        parents.append(p3[0])
        aux.remove(p3[0])
    else:
        parents.append(p3[1])
        aux.remove(p3[1])
    p4=rand.sample(aux,2)
    if(p4[0][1]> p4[1][1]):
        parents.append(p4[0])
        aux.remove(p4[0])
    else:
        parents.append(p4[1])
        aux.remove(p4[1]) 
    #print(parents)
    return parents

def crossOver(parents):
    sind12= rand.randint(0,4)
    eind12=rand.randint(0,4)
    sind34= rand.randint(0,4)
    eind34=rand.randint(0,4)
    
    offs1=[]
    offs2=[]
    offs3=[]
    offs4=[]
    
    
    offs1[sind12:eind12+1]=parents[0][0][sind12:eind12+1]
    offs2[sind12:eind12+1]=parents[1][0][sind12:eind12+1]
    offs3[sind34:eind34+1]=parents[2][0][sind34:eind34+1]
    offs4[sind34:eind34+1]=parents[3][0][sind34:eind34+1]
    
    auxind=eind12+1
    while (1):
        if (sind12 == 0 and auxind==4):
            break
        else:
            if(parents[1][0][auxind%5] not in offs1):
                if(auxind%5==sind12): break
                offs1[auxind%5]= parents[1][0][auxind%5]
                auxind+=1
        
    auxind=eind12+1
    while (1):
        if (sind12 == 0 and auxind==4):
            break
        else:
            if(parents[0][0][auxind%5] not in offs2):
                if(auxind%5==sind12): break
                offs2[auxind%5]= parents[0][0][auxind%5]
                auxind+=1
    auxind=eind34+1
    while (1):
        if (sind34 == 0 and auxind==4):
            break
        else:
            if(parents[3][0][auxind%5] not in offs3):
                if(auxind%5==sind34): break
                offs3[auxind%5]= parents[3][0][auxind%5]
                auxind+=1
    auxind=eind34+1
    while (1):
        if (sind34 == 0 and auxind==4):
            break
        else:
            if(parents[2][0][auxind%5] not in offs4):
                if(auxind%5==sind34): break
                offs4[auxind%5]= parents[2][0][auxind%5]
                auxind+=1
    crossOffsprings= [offs1,offs2, offs3, offs4]
    return crossOffsprings

#mutate if in probability
def insertMutations(crossOffsprings):
    probability= round(rand.random(),2)
    if(probability<=0.20):
        for mut in crossOffsprings:
            m1=rand.randint(0,5)
            m2=rand.randint(0,5)
            remv=mut.remove(mut[m2])
            mut.insert((m1+1)%5,remv)
    else:
        return crossOffsprings
    return crossOffsprings

def survivalSelection(mutCross, parents):
    costOffspring=fitnessFunction(mutCross)
    for i in range(len(costOffspring)):
        parents.append(costOffspring[i])
    finalParents= addC(parents)
    finalParents=sorted(finalParents, key= lambda x: x[2])
    finalParents=finalParents[4:]
    return finalParents

def addC(parents):
    c=[]
    for i in parents:
       c.append(i[0].insert(0, 'C')) 
    finalParents= fitnessFunction(c)
    return finalParents

def removeC(parents):
    c=[]
    for i in parents:
       c.append(i[0].remove('C')) 
    finalParents= fitnessFunction(c)
    return finalParents

def bestSoFar(finalParents):
    bestFitness=finalParents[-1][1]
    return bestFitness

def averageBest(finalParents):
    sumd=0
    for i in finalParents:
        sumd+= i[1]
    return sumd/6
    
if __name__=='main':
    main()
    
    
    
    