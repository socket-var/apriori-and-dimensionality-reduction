import re
import sys

# Prune one element subset 
def getPrunedData(Items,Data,minSup):
	pruned = []
	for i in Items:
		count = 0
		for entry in Data:
			if(i in entry):
				count+=1
		# print(count)
		sup = float(count)/len(Data)
		# print(sup)
		if(sup>=minSup):
			pruned.append(i)
	return(pruned)

# Checks support for any given item
def checkSupport(subItem,Data,minSup):
	count = 0
	for superset in Data:
		result = all(elem in superset for elem in subItem)
		if(result):
			count+=1

	sup = float(count)/len(Data)
	if(sup>=minSup):
		return(True)
	else:
		return(False)

# Generate Two item subsets
def generateTwoItemSubset(Items,minSup):
	twoItem = []
	for i in range(len(Items)):
		for j in range(i+1,len(Items)):
			subset = [Items[i],Items[j]]
			if(checkSupport(subset,Data,minSup)):
				twoItem.append([Items[i],Items[j]])
	return(twoItem)

# Generates subsets of any length
def generateSubsets(Items,Data,minSup):
	newItems=[]
	newItem = []
	for i in range(0,len(Items)):
		for j in range(i+1,len(Items)):
			if(checkItems(Items[i],Items[j])):
				newItem.extend(Items[i])
				newItem.append(Items[j][-1])
				#print(newItem)
				if(checkSupport(newItem,Data,minSup)):
					newItems.append(newItem)
				newItem = []
			else:
				break
	return newItems

# Checks the prefix
def checkItems(firstItem,secondItem):
	for i in range(0,len(firstItem)-1):
		if(firstItem[i]!=secondItem[i]):
			return False
	return True

# Reading data from given text file
file = open("associationruletestdata.txt","r")
filecontent = file.readlines();
Data = []
Items = []
Frequent = []
min = sys.maxsize
minSup = float(sys.argv[1])
for fileline in filecontent:
	line = fileline.split('\t')
	line[-1] = line[-1][:-2]
	for i in range(0,len(line)-1):
		#adding 'Gi_' prefix to all gene sequences
		line[i] = "G"+str(i+1)+"_"+line[i]
	Data.append(line)

for i in range(0,len(Data[0])-1):
	if(Data[0][i] == "G"+str(i+1)+"_"+"Up"):
		Items.append(Data[0][i])
		Items.append("G"+str(i+1)+"_"+"Down")
	elif(Data[0][i] == "G"+str(i+1)+"_"+"Down"):
		Items.append("G"+str(i+1)+"_"+"Up")
		Items.append(Data[0][i])

for line in Data:
	if(line[-1] not in Items):
		Items.append(line[-1])

# Contains all the unique items from all transactions
# print(Items)
# print("Length of Unique items:"+str(len(Items)))

Items = getPrunedData(Items,Data,minSup)

Frequent.extend(Items)
# print(Items)
print(1,len(Items))

twoItem = generateTwoItemSubset(Items,minSup)
Frequent.extend(twoItem)
# print(twoItem)
print(2,len(twoItem))
# print(len(Frequent))

# Generate all other subsets from two item subsets
Items = twoItem
subSetLen = 3
while(True):
	Items = generateSubsets(Items,Data,minSup)
	if(len(Items) == 0):
		break
	print(subSetLen,len(Items))
	subSetLen+=1
	Frequent.extend(Items)
print("Length of frequent Itemsets")
print(len(Frequent))
