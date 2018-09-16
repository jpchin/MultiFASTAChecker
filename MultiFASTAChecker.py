import plotly as py
import plotly.graph_objs as go
import statistics
import math

import tkinter as tk
from tkinter import filedialog
root = tk.Tk()
root.withdraw()

gettingLocation = True
while (gettingLocation == True):
    print("\nPlease choose an input file with FASTA sequences: ")
    #Get a file location, set as inputFASTALocation
    inputFASTALocation = filedialog.askopenfilename()
    #Try to open the file, if successful set as FASTAData
    try:
        inputFile = open(inputFASTALocation,"r")
        gettingLocation = False
    #If opening the file fails alert the user and try again
    except IOError:
        print("Sorry, I'm unable to open that file location.")


gettingLocation = True
while (gettingLocation == True):
    print("\nPlease choose an output file location and file name: ")
    outputFileLocation = filedialog.asksaveasfilename()
    try:
        file = open(outputFileLocation,"w")
        gettingLocation = False
    except IOError:
        print("Sorry, I'm unable to open that file location.")

#Open the input file, read into a single large string
#with open (inputFile, "r") as file:
data = inputFile.read()

#Quick number check
numSeqs = data.count(">")
print("There are " + str(numSeqs) + " sequences in the input file")

#A list to hold all of the important data
seqsList = []

#A few variables to store search positions
lastSeq = 0
seqEnd = 0
for x in range (0, numSeqs):
    #Find the next sequence
    seqEnd = data.find(">", seqEnd+1)
    sequence = data[lastSeq:seqEnd]

    #Find the end of the header in the sequence
    headerEnd = sequence.find("\n")

    #Create a dictionary containing different elements for the header and the
    #amino acid seuqence, add this to seqsList.
    dictionary = {"header":sequence[:headerEnd],
                  "sequence":sequence[headerEnd:].replace("\n", "")}
    seqsList.append(dictionary)

    #Start the next search at the end of the last search
    lastSeq = seqEnd
         
#Append the length of each amino acid sequence to each item in seqsList
for sequence in seqsList:
    sequence["length"] = len(sequence["sequence"])

#Sort the sequences by length
seqsList = sorted(seqsList, key=lambda k: k["length"])

#Create a list to hold lengths, append the length of each seq to it
###This will be Y axis data for a bar chart###
lengthList = []
for seq in seqsList:
    lengthList.append(seq["length"])

#Create a list to hold sequence names, append names to it
###This will be X axis labels for a bar chart###
headerList = []
for seq in seqsList:
    headerList.append(seq["header"])
    
Avg = sum(lengthList) / numSeqs
print(Avg)
CI = statistics.stdev(lengthList)  * 1.96
print(CI)
upper = Avg + CI
lower = Avg - CI
print(str(lower) + " - " + str(upper))

colours = []
for x in range (0, numSeqs):
    if ((lower > seqsList[x]["length"]) or (upper < seqsList[x]["length"])):
        colours.append('rgb(255, 64, 64)')
    else:
        colours.append('rgb(32,16,128)')


data = [go.Bar(x=headerList,y=lengthList,marker=dict(color=colours))]
py.offline.plot(data, filename="chart.html")

shortest = int(input("\nWhat's the shortest sequence *You want*? "))
longest = int(input("\nWhat's the longest sequence *You want*? "))

outputseqs = []

for seq in seqsList:
    if ((seq["length"] >= shortest) and (seq["length"] <= longest)):
        outputseqs.append(seq)

print("There are " + str(len(outputseqs)) + " seqs in the output list")

"""
with open(outputFileLocation, "w") as file:
    for seq in outputseqs:
        file.write(seq["header"] + "\n")
        length = math.ceil(len(seq["header"]))
        outputString = ""
        for x in range (0, length):
            outputString += (seq["sequence"][0+(80*x):80+(80*x)])
        file.write(outputString)
"""

with open(outputFileLocation, "w") as file:
    for seq in outputseqs:
        file.write(seq["header"] + "\n" + seq["sequence"] + "\n")
       
