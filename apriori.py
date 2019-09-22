import re
import sys

# Reading data from given text file
file = open("associationruletestdata.txt","r")
filecontent = file.readlines();
Data = []
Items = []
min = sys.maxsize
for fileline in filecontent:
	line = fileline.split('\t')
	line[-1] = line[-1][:-1]
	for i in range(0,len(line)-1):
		#adding 'Gi_' prefix to all gene sequences
		line[i] = "G"+str(i+1)+"_"+line[i]
	Data.append(line)

for i in range(0,len(Data[0])-1):
	#print(Data[0][i],"G"+str(i+1)+"_"+"Up")
	if(Data[0][i] == "G"+str(i+1)+"_"+"Up"):
		print(Data[0][i],"G"+str(i+1)+"_"+"Up")
		Items.append(Data[0][i])
		Items.append("G"+str(i+1)+"_"+"Down")
	elif(Data[0][i] == "G"+str(i+1)+"_"+"Down"):
		Items.append("G"+str(i+1)+"_"+"Up")
		Items.append(Data[0][i])

for line in Data:
	if(line[-1] not in Items):
		Items.append(line[-1])

# Contains all the unique items from all transactions
print(Items)
print("Length of Unique items:"+str(len(Items)))

'''
subsets = []
for i in range(1,len(Items)):
	subsets = list(itertools.combinations(Items,i))
	with open('subsets.txt','a') as file:
		for item in subsets:
			file.write("{}\n".format(list(item)))
	print("Done with subsets of length "+str(i))
'''