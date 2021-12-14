#This code is adapted from Adam Bricker's teaching materials 


import pandas as pd
from scipy.stats import norm
from os import listdir

#d' function
def dPrime(hitRate, FArate):
    stat = norm.ppf(hitRate) - norm.ppf(FArate)

    return stat

#criterion function
def criterion(hitRate, FArate):
    stat = -.5*(norm.ppf(hitRate) + norm.ppf(FArate))

    return stat

#import the raw data from the csv file
dataPath = "data/group_fixed/"
fileList = listdir(dataPath)
fileList.remove('.DS_Store') #removing the hidden file in mac folder

#checking the list
#print(fileList)

#the data frame we'll be using
accuracy = pd.DataFrame({"condition" : ["coffee_a", "coffee_b"], "hits" : [0,0], "misses" : [0,0],
                        "CRs" : [0,0], "FAs" : [0,0]})

for dataFile in fileList:
    rawData = pd.read_csv(dataPath + dataFile, delimiter = ";", encoding="latin-1" )


#make a new data frame only with the data we need
    expData = pd.DataFrame(rawData, columns = ["Condit", "Task", "key_resp.keys", "key_resp.rt"])

#rename to make things easier
    expData = expData.rename(columns = {"Condit" : "condition", "Task" : "task",
                "key_resp.keys" : "resp", "key_resp.rt" : "RT"})
    
##calculate hit, false alarm, correct rejection, and miss rates (for each condition)
#updating the data frame for each entry
    for index, row in expData.iterrows():
    #condition: low
        if row["condition"] == "coffee_a":
            rowInd = 0
        #Hit
            if row["task"] == "go" and row["resp"] == "space":
                accuracy.loc[rowInd,"hits"] += 1
        #Miss
            elif row["task"] == "go" and row["resp"] == "None":
                accuracy.loc[rowInd,"misses"] += 1
        #Correct rejection
            elif row["task"] == "no-go" and row["resp"] == "None":
                accuracy.loc[rowInd,"CRs"] += 1
        #False alarm
            elif row["task"] == "no-go" and row["resp"] == "space":
                accuracy.loc[rowInd,"FAs"] += 1

    #condition: high
        elif row["condition"] == "coffee_b":
            rowInd = 1
        #Hit
            if row["task"] == "go" and row["resp"] == "space":
                accuracy.loc[rowInd,"hits"] += 1
        #Miss
            elif row["task"] == "go" and row["resp"] == "None":
                accuracy.loc[rowInd,"misses"] += 1
        #Correct rejection
            elif row["task"] == "no-go" and row["resp"] == "None":
                accuracy.loc[rowInd,"CRs"] += 1
        #False alarm
            elif row["task"] == "no-go" and row["resp"] == "space":
                accuracy.loc[rowInd,"FAs"] += 1


print(accuracy)

#Calculate rates from response counts (8 files)
hitRate_coffee_a = accuracy.loc[0]["hits"]/(15*8) 
FArate_coffee_a = accuracy.loc[0]["FAs"]/(15*8)

hitRate_coffee_b = (accuracy.loc[1]["hits"]-1)/(15*8) #corrected to be less than 1
FArate_coffee_b = (accuracy.loc[1]["FAs"])/(15*8)

#Calculate d' and criterion
print("d' (coffee_a):", dPrime(hitRate_coffee_a, FArate_coffee_a))
print("criterion (coffee_a):", criterion(hitRate_coffee_a, FArate_coffee_a))

print("d' (coffee_b):", dPrime(hitRate_coffee_b, FArate_coffee_b))
print("criterion (coffee_b):", criterion(hitRate_coffee_b, FArate_coffee_b))


