#This code is adapted from Adam Bricker's teaching materials


import pandas as pd
import matplotlib.pyplot as plt

from statistics import mean
from os import listdir
from statsmodels.stats.anova import AnovaRM


##import data
dataPath = "data/group_fixed/"
fileList = listdir(dataPath)
fileList.remove('.DS_Store') #removing the hidden file in mac folder

#checking the list
#print(fileList)
    

#data frame for mean RTs
meanRTs = pd.DataFrame({"participant" : [], "Task" : [], "Condit" : [], "key_resp.keys" : [],
                    "mean RT" : [] })

counter = 0
for dataFile in fileList:
    
#New ID for each participant
    counter += 1
    pNum = "P-" + str(counter)
    rawData = pd.read_csv(dataPath + dataFile, delimiter = ";", encoding="latin-1")
#checking the dataframe
    #print(rawData)

    expData = pd.DataFrame(rawData, columns = ["Task", "Condit", "key_resp.keys", "key_resp.rt"])
    
    expData = expData.rename(columns = {"key_resp.rt" : "RT", "key_resp.keys" : "response", "Condit" : "condition"})
    
    
#only include trials with a response
    rtData = expData[expData.RT.notnull()]
    
    #print(rtData.to_string())
    
    #only two conditions (coffee_a & coffee_b go's):
    #data frame for RTs for each condition
    coffee_a_RTs = rtData[(rtData.condition == "coffee_a")].RT
    coffee_b_RTs = rtData[(rtData.condition == "coffee_b")].RT
    
    #new data to add to meanRTs
    pNumList = [pNum, pNum]
    condList = ["coffee_a", "coffee_b"]

    meanRTsList = [mean(coffee_a_RTs), mean(coffee_b_RTs)]  

    #new data --> data frame
    newLines = pd.DataFrame({"participant" : pNumList, "Condit" : condList, "mean RT" : meanRTsList})

    #append newLines to meanRTs
    #(note: unlike appending a list, this doesn't change the initial data frame)
    meanRTs = meanRTs.append(newLines, ignore_index=True) #don't want index duplicates

#print(meanRTs) 

#group means
coffee_a_Means = meanRTs[(meanRTs.Condit == "coffee_a")]["mean RT"]
coffee_b_Means = meanRTs[(meanRTs.Condit == "coffee_b")]["mean RT"]


print("coffee_a, mean RT:", mean(coffee_a_Means))
print("coffee_b, mean RT:", mean(coffee_b_Means))

    
#visualization:    

fig, ax = plt.subplots()

box = ax.boxplot([coffee_a_Means, coffee_b_Means])

ax.set_ylabel("RT (s)")
ax.set_xticklabels(["coffee_a: condition1 (dissimilar) ", "coffee_b: condition2 (similar) "])

plt.show()

#repeated measures anova
model = AnovaRM(data = meanRTs, depvar = "mean RT", subject = "participant", within = ["Condit"]).fit()
print(model)
