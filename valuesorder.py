import pandas as pd
import random
import json

def get_combinations(list):
    result = []
    for i in range(len(list)):
        for j in range(i + 1, len(list)):
            result.append((list[i], list[j]))
    return result

def remove_item(list:list, item):
    newList = list[:]
    newList.remove(item)
    return newList

data = pd.read_csv('data.csv',sep=',', header=0, encoding='UTF-8', usecols=['Wartosc','Opis'])
listOfValues = data['Wartosc'].tolist()
describeOfValues = data['Opis'].tolist()
dictOfValues = {listOfValues[i]: describeOfValues[i] for i in range(len(listOfValues))}

choice = input("Continue (c) or start from beginning (b)")

if choice == 'c':
    f = open('save.json')
    devDict = json.load(f)
    f.close()
    devListOfValues =[]
    for i in devDict:
        if len(devDict[i][2]) != 0:
            devListOfValues.append(i)
elif choice == 'b':
    devDict = {listOfValues[i]: [0, 1, remove_item(listOfValues,listOfValues[i])] for i in range(len(listOfValues))}
    devListOfValues = [i for i in devDict.keys()]

while True:
    a = random.choices(devListOfValues,[devDict[i][1] for i in devListOfValues])[0]
    print(f'A: {a} - {dictOfValues[a]}')
    index = devListOfValues.index(a)
    b = random.choices(devDict[a][2],[devDict[i][1] for i in devDict[a][2]])[0]
    print(f'B: {b} - {dictOfValues[b]}')
    answer = input("What do you chose(A, B, q-quit):")
    if answer == 'q':
        break
    elif answer == 'A' or answer == 'a':
        devDict[a] = [devDict[a][0]+1,devDict[a][1]*0.9,remove_item(devDict[a][2], b)]
        devDict[b] = [devDict[b][0]-1,devDict[b][1]*0.8,remove_item(devDict[b][2], a)]
    elif answer == 'B' or answer == 'b':
        devDict[a] = [devDict[a][0]-1,devDict[a][1]*0.8,remove_item(devDict[a][2], b)]
        devDict[b] = [devDict[b][0]+1,devDict[b][1]*0.9,remove_item(devDict[b][2], a)]
    elif answer == 's':
        with open('save.json', 'w') as fp:
            json.dump(devDict, fp)
        break
    elif answer == 'w':
        data['Score'] = [devDict[i][0] for i in devDict]
        data.to_csv('data.csv')
        with open('save.json', 'w') as fp:
            json.dump(devDict, fp)
        break
    elif answer == 'p':
        score = [devDict[i][0] for i in devDict]
        prop = [devDict[i][1] for i in devDict]
        print(score)
        print(prop)

    if len(devDict[a][2]) == 0:
        devListOfValues.remove(a)
    if len(devDict[b][2]) == 0:
        devListOfValues.remove(b)
    if len(devListOfValues) == 0:
        data['Score'] = [devDict[i][0] for i in devDict]
        data.to_csv('data.csv')
        break
