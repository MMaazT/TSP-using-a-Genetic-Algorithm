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
    #print(permut)
    best=[]
    average=[]
    for i in range(100):
        initialTourCost= fitnessFunction(permut)
        parents=parentSelection(initialTourCost)
        crossed= crossOver(parents)
        mut=insertMutations(crossed)
        tenBest= survivalSelection(mut, initialTourCost)
        bo=(bestSoFar(tenBest))
        a=(averageBest(tenBest))
        permut=removeC(tenBest)
        best.append(bo)
        average.append(round(a,5))
        #print(i, a)
        #print(i, bo)
    print(best)
    print(average)
    #plt.plot(best)
    plt.plot(average)
    
    

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

        
    sind12= rand.randint(0,3)
    eind12=rand.randint(sind12,4)
    if(sind12==eind12):
        eind12+=1
    sind34= rand.randint(0,3)
    eind34=rand.randint(sind34,4)
    if(sind34==eind34):
        eind34++1
   # print(sind12,eind12,sind34,eind34)
    
    offs1=[0,0,0,0,0]
    offs2=[0,0,0,0,0]
    offs3=[0,0,0,0,0]
    offs4=[0,0,0,0,0]
    
    
    offs1[sind12:eind12+1]=parents[0][0][sind12:eind12+1]
    #print(offs1)
    offs2[sind12:eind12+1]=parents[1][0][sind12:eind12+1]
    #print(offs2)
    offs3[sind34:eind34+1]=parents[2][0][sind34:eind34+1]
    #print(offs3)
    offs4[sind34:eind34+1]=parents[3][0][sind34:eind34+1]
    #print(offs4)
    
    
    auxparent2=parents[1][0][eind12:]
    auxparent2= auxparent2 + parents[1][0][:eind12]
    #print(auxparent2)
    auxind=eind12
    for j in range(len(auxparent2)):
        if(auxparent2[j] not in offs1):
            auxind+=1
            offs1[auxind%5]=auxparent2[j]
    
    
    auxparent1=parents[0][0][eind12:]
    auxparent1= auxparent1 + parents[0][0][:eind12]
   
    auxind=eind12
    for j in range(len(auxparent1)):
        if(auxparent1[j] not in offs2):
            auxind+=1
            offs2[auxind%5]=auxparent1[j]
    
    auxparent4=parents[3][0][eind34:]
    auxparent4= auxparent4 + parents[3][0][:eind34]
    
    auxind=eind34
    for j in range(len(auxparent4)):
        if(auxparent4[j] not in offs3):
            auxind+=1
            offs3[auxind%5]=auxparent4[j]
    
    auxparent3=parents[2][0][eind34:]
    auxparent3= auxparent3 + parents[2][0][:eind34]
   
    auxind=eind34
    for j in range(len(auxparent3)):
        if(auxparent3[j] not in offs4):
            auxind+=1
            offs4[auxind%5]=auxparent3[j]
    """
    auxind=eind12+1
    par2ind=eind12+1
    while (par2ind%5!=eind12%5+1):
        
        if(parents[1][0][par2ind%5] not in offs1):
            offs1[auxind%5]= parents[1][0][par2ind%5]
            auxind+=1
            par2ind+=1
        else: par2ind+=1
        
    auxind=eind12+1
    par1ind=eind12+1
    while (par1ind%5!=eind12%5+1):
   
        if(parents[0][0][par1ind%5] not in offs2):
            offs2[auxind%5]= parents[0][0][par1ind%5]
            auxind+=1
            par1ind+=1
        else: par1ind+=1
    
    auxind=eind34+1
    par4ind=eind34+1
    while (par4ind%5!=eind34%5+1):
    
        if(parents[3][0][par4ind%5] not in offs3):
            offs3[auxind%5]= parents[3][0][par4ind%5]
            auxind+=1
            par4ind+=1
        else: par4ind+=1
    
    auxind=eind34+1
    par3ind=eind34+1
    while (par3ind%5!=eind34%5+1):
        
        if(parents[2][0][par3ind%5] not in offs4):
            offs4[auxind%5]= parents[2][0][par3ind%5]
            auxind+=1
            par3ind+=1
        else: par3ind+=1
    """

    crossOffsprings= [offs1,offs2, offs3, offs4]
    #print (crossOffsprings)
    return crossOffsprings

#mutate if in probability
def insertMutations(crossOffsprings):
    probability= round(rand.random(),2)
    if(probability<=0.20):
        for mut in crossOffsprings:
            m1=rand.randint(0,2)
            m2=rand.randint(3,4)
            mut.insert(m1+1,mut[m2])
            mut.remove(mut[m2+1])
            
    else:
        return crossOffsprings
    return crossOffsprings

def survivalSelection(mutCross, parents):
    costOffspring=fitnessFunction(mutCross)
    parents=parents+costOffspring
    finalParents= addC(parents)
    finalParents=sorted(finalParents, key= lambda x: x[1])
    finalParents=finalParents[:10]
    return finalParents

def addC(parents):
    c=[]
    for i in parents:
       i[0].insert(0, 'C')
    for i in parents:
        c.append(i[0])
    finalParents= fitnessFunction(c)
    return finalParents

def removeC(parents):
    c=[]
    for i in parents:
        i[0].remove('C') 
    for i in parents:
        c.append(i[0]) 
    #finalParents= fitnessFunction(c)
    return c

def bestSoFar(finalParents):
    bestFitness=finalParents[0][1]
    return bestFitness

def averageBest(finalParents):
    sumd=0
    for i in finalParents:
        sumd+= i[1]
    return sumd/6
    
if __name__=='main':
    main()
    
    
    
    