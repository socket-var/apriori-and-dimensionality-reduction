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
		sup = float(count)/len(Data)
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
	#print("level one")
	#print(FreqItem)
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

# Generate all the levels other than the first level
def generateOtherLevels(FreqItem,left,right,level):
	newleft = []
	newright = []
	#print("next level "+str(level))
	#print(left)
	#print(right)
	for i in range(0,len(left)):
		for j in range(i+1,len(left)):
			comleft = getCommonLeft(left[i],left[j])
			comright = getCommonRight(right[i],right[j])
			#print(comleft,comright)
			if(len(comleft)>0):
				if(checkConfidence(comleft,FreqItem)):
					#print(comleft,comright)
					if(comleft not in newleft):
						newleft.append(comleft)
						newright.append(comright)
	return(newleft,newright)

# Gets the intersection of elements for left
def getCommonLeft(left1,left2):
	cleft = []
	l1 = set(left1)
	l2 = set(left2)
	cleft = sortList(list(l1&l2))
	return cleft

# Gets the Union of elements for right
def getCommonRight(right1,right2):
	cright = [] 
	r1 = set(right1)
	r2 = set(right2)
	cright = sortList(list(r1.union(r2)))
	return cright

# Sort left list or right list based on numbers in the string
def sortList(toSort):
	d = {}
	#print("In toSort")
	temp = []
	for i in range(0,len(toSort)):
		if(toSort[i][1].isdigit()):
			num = re.findall(r'\d+',toSort[i])
			#print("key: ",num,"string: ",toSort[i])
			d[int(num[0])] = toSort[i]
		else:
			temp.append(toSort[i])
	ans = [val[1] for val in sorted(d.items(),key = lambda x:x[0])]
	ans.extend(temp)
	return ans

# Check confidence
def checkConfidence(templeft,FreqItem):
	keyFreqItem = "-".join(FreqItem)
	if(len(templeft) == 1):
		keyLeft = templeft[0]
	else:
		keyLeft = "-".join(templeft)
	conf = float(Frequency[keyFreqItem])/Frequency[keyLeft]
	#print(conf)
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
print(1,len(Items))
oneItemLen = len(Items)

twoItem = generateTwoItemSubset(Items,minSup)
Frequent.extend(twoItem)
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

### Part 2 ###

Gleft = []
Gright = []


for i in range(oneItemLen,len(Frequent)):
	left = []
	right = []
	# if(len(Frequent[i])==6):
	# 	print(Frequent[i])
	# 	continue
	if(len(Frequent[i])>=2):
		(newleft,newright) = generateLevelOneRules(Frequent[i],left,right)
		Gleft.extend(newleft)
		Gright.extend(newright)
	if(len(Frequent[i])==2):
		continue
	for j in range(0,len(Frequent[i])-2):
		(newleft,newright) = generateOtherLevels(Frequent[i],newleft,newright,j+2)
		Gleft.extend(newleft)
		Gright.extend(newright)
	


#Print Utility

#for i in range(0,len(Gleft)):
# 	print(Gleft[i],Gright[i])
print("Length of rules generated")
print(len(Gleft))

# frequentItem = ['G8_Up', 'G24_Down', 'G54_Up', 'G80_Down', 'G81_Up', 'Breast Cancer']
# left = []
# right = []
# (newleft,newright) = generateLevelOneRules(frequentItem,left,right)
# print(newleft)
# print(newright)
# for j in range(0,len(frequentItem)-2):
# 	if(j+2 == 5):
# 		break
# 	(newleft,newright) = generateOtherLevels(frequentItem,newleft,newright,j+2)
# 	print("Level "+ str(j+2))
# 	print(newleft)
# 	print(newright)
# 	print(len(newleft))
# 	print(len(newright))




