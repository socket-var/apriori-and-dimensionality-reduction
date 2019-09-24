import re
import sys
import collections

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
			Frequency[i] = count
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
		key = "-".join(subItem)
		Frequency[key] = count
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

###################################################

# Generate level one association rules for given frequent item
def generateLevelOneRules(FreqItem,left,right):
	print(FreqItem)
	for i in range(0,len(FreqItem)):
		templeft = []
		tempright = []
		for j in range(0,len(FreqItem)):
			if(i==j):
				tempright.append(FreqItem[i])
			else:
				templeft.append(FreqItem[j])
		#print(templeft,tempright)
		if(checkConfidence(templeft,FreqItem)):
			left.append(templeft)
			right.append(tempright)
	return(left,right)

def generateOtherLevels(left,right):
	newLeft = []
	newRight = []
	return(newLeft,newRight)

# Check confidence
def checkConfidence(templeft,FreqItem):
	keyFreqItem = "-".join(FreqItem)
	if(len(templeft) == 1):
		keyLeft = templeft[0]
	else:
		keyLeft = "-".join(templeft)
		#print(keyFreqItem,keyLeft)
	conf = float(Frequency[keyFreqItem])/Frequency[keyLeft]

	if(conf>=minConf):
		return True
	else:
		return False

### Part 1 ###
# Reading data from given text file
file = open("associationruletestdata.txt","r")
filecontent = file.readlines();
Data = []
Items = []
Frequent = []
Frequency = collections.OrderedDict()
min = sys.maxsize
minSup = float(sys.argv[1])
minConf = float(sys.argv[2])
for fileline in filecontent:
	line = fileline.split('\t')
	line[-1] = line[-1][:-1]
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
oneItemLen = len(Items)

twoItem = generateTwoItemSubset(Items,minSup)
Frequent.extend(twoItem)
# print(twoItem)
print(2,len(twoItem))

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
print("Length of support dictionary")
print(len(Frequency))
#print(Frequency)

### Part 2 ###

Gleft = []
Gright = []

for i in range(oneItemLen,len(Frequent)):
	#print(len(Frequent))
	left = []
	right = []
	if(len(Frequent[i])>=2):
		(newleft,newright) = generateLevelOneRules(Frequent[i],left,right)
		Gleft.extend(newleft)
		Gright.extend(newright)
	if(len(Frequent[i])==2):
		continue
	if(len(Frequent[i])==4):
		break
	# for j in range(0,len(Frequency[i])-2):
	# 	(left,right) = generateOtherLevels(left,right)

#Print Utility

for i in range(0,len(Gleft)):
	print(Gleft[i],Gright[i])
print(len(Gleft))


