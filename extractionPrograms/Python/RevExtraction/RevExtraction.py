from CardExtractor import *
import uuid
import os

temp = "DMX-22_Super_Black_Box_Pack"
cardLimit = 1000

def extractSet(setName = "kek"):

	setQuery = 'https://duelmasters.fandom.com/api.php?action=query&prop=revisions&rvprop=content&format=php&titles=' + setName
	with urllib.request.urlopen(setQuery) as response:
		html = response.read().decode('utf-8')

	i = html.find("==Contents==")
	if(i == -1):
		print("==Contents== not found. Looking for Contents== now")
		i = html.find("Contents==")
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
	html = html.replace("<br>", "\n") #sometimes a and b sides are on the same line, separated by <br>

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

			try:
				cardXML = cardXML + extractCardData(cardName, setName)
			except:
				cardXML = cardXML + "\n ERROR EXTRACTING DATA FROM CARD "+cardName+" \n"

		cardLimit -= 1
		if cardLimit < 0:
			break

	return cardXML


def createSetXML(setName):
	setTemplateFile = open("SetTemplate.txt", "r")
	setXML = setTemplateFile.read()

	setNameTemp =  setName.replace("_", " ").replace("\"", "\'")         # double quotes in xml will cause problems
	setXML = setXML.replace("SET_NAME_REPLACE", setNameTemp)

	setXML = setXML.replace("SET_ID_REPLACE", str(uuid.uuid4()))
	setXML = setXML.replace("BOOSTER_ID_REPLACE", str(uuid.uuid4()))

	cardXML = extractSet(setName, cardLimit)
	setXML = setXML.replace("CARDS_REPLACE", cardXML)
	print("Set xml is:\n"+setXML)

	setFile = open("setData_" + setName[0:6] + ".xml", 'w', encoding='utf-8')
	setFile.write(setXML)
	setFile.close()






createSetXML(temp)
# extractSet(temp)
