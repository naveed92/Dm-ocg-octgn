from CardExtractor import *
import uuid
import os

temp = "DMR-17_Burning_Dogiragon!!"


def extractSet(setName = "kek"):

	setQuery = 'https://duelmasters.fandom.com/api.php?action=query&prop=revisions&rvprop=content&format=php&titles=' + setName
	with urllib.request.urlopen(setQuery) as response:
		html = response.read().decode('utf-8')

	i = html.find("==Contents==")
	j = -1

	endingKeywords = ["==Cycles==", "==Contents sorted by Civilizations==", "==Gallery==",  "==Trivia=="]
	for keyword in endingKeywords:
		j = html.find(keyword)
		if j > 0:
			print("Ending keyword found:"+keyword)
			break
	if j == -1:
		print("WARNING: No contents ending keyword found in set data, processing everything after ==Contents==")

	html = html[i:j]

	lines = html.split("\n")
	cardCount = 1
	cardXML = ""

	###################### Make images folder for set #####################

	dirName = setName[0:6]+"-Images"
	try:
		os.mkdir(dirName)
		print("Directory ", dirName, " Created ")
	except FileExistsError:
		print("Directory ", dirName, " already exists")

	for line in lines:
		i = line.find("[[")
		j = line.find("]]")

		if i > 0 and j > 0:
			i = i + 2
			cardName = line[i:j].replace(" ", "_")
			print("\n"+str(cardCount) + " Card is: "+ cardName)
			cardCount+= 1

			cardXML = cardXML + extractCardData(cardName, setName)

	return cardXML


def createSetXML(setName):
	setTemplateFile = open("SetTemplate.txt", "r")
	setXML = setTemplateFile.read()

	setNameTemp =  setName.replace("_", " ").replace("\"", "\'")         # double quotes in xml will cause problems
	setXML = setXML.replace("SET_NAME_REPLACE", setNameTemp)

	setXML = setXML.replace("SET_ID_REPLACE", str(uuid.uuid4()))
	setXML = setXML.replace("BOOSTER_ID_REPLACE", str(uuid.uuid4()))

	cardXML = extractSet(setName)
	setXML = setXML.replace("CARDS_REPLACE", cardXML)
	print("Set xml is:\n"+setXML)

	setFile = open("setData_"+setName[0:6]+".xml", "w")
	setFile.write(setXML)
	setFile.close()






createSetXML(temp)
# extractSet(temp)
