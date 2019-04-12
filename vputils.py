import time
import random

def randomizeListWithWeight(list):
    # list is a list with an item and a weight for that item
    # it returns a list of the items with the number of items in the newlist determined by the weight
    newList = []
    for item in list:
        func = item[0]
        repeat = item[1]
        for x in range(0, repeat):
            newList.append(func)
    return newList

def chooseRandomFunction(list):
    x = random.randrange(0,len(list))
    return list[x]

def reducedFunctionList(functionList,func,super):
    newList = []
    for listItem in functionList:
        if listItem != func:
            newList.append(listItem)
    if len(newList):
        return newList
    else: 
        return randomizeListWithWeight(super.weightedList())