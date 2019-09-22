import re
import sys

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
			if(Items[i][:3]!=Items[j][:3]):
				subset = [Items[i],Items[j]]
				if(checkSupport(subset,Data,minSup)):
					twoItem.append([Items[i],Items[j]])
	return(twoItem)

# Reading data from given text file
file = open("associationruletestdata.txt","r")
filecontent = file.readlines();
Data = []
Items = []
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
	#print(Data[0][i],"G"+str(i+1)+"_"+"Up")
	if(Data[0][i] == "G"+str(i+1)+"_"+"Up"):
		# print(Data[0][i],"G"+str(i+1)+"_"+"Up")
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
# print(Items)
# print(len(Items))

twoItem = generateTwoItemSubset(Items,minSup)
# print(twoItem)
print(len(twoItem))




'''
subsets = []
for i in range(1,len(Items)):
	subsets = list(itertools.combinations(Items,i))
	with open('subsets.txt','a') as file:
		for item in subsets:
			file.write("{}\n".format(list(item)))
	print("Done with subsets of length "+str(i))
'''