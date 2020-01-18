import urllib.request
import urllib.parse
import uuid


temp = "Barrier of Revolution"
temp2 = "DMR-17_Burning_Dogiragon!!"

def extractCardData(cardName, setName=""):
	cardNameURL = urllib.parse.quote(cardName)
	with urllib.request.urlopen('https://duelmasters.fandom.com/api.php?action=query&prop=revisions&rvprop=content&format=php&titles='+cardNameURL) as response:
		html1 = response.read().decode('utf-8')

	html=""
	html = str(html1)

	i = html.find('{{Cardtable') +11
	j = html.rfind('}}')
	if j == -1:
		j = html.find('[[Category:')
	html = html[i:j]

	#print("Point 1, HTML is :\n"+html)

	##### Getting all the data #######
	#Note to self - image can be gotten through query, check the other program with Yomi
	name = cardName.replace("_", " ")

	cost = getAttribute("cost", html)
	if cost is None:
		print("ERROR: No cost found!")
		return "ERROR NO COST FOUND ON CARD " + cardName

	civ = getAttribute("civilization", html)
	if civ is None:
		print("WARNING: No civ found! Assigning Zero.")
		civ = "Zero"

	power = getAttribute("power", html)
	if power is None:
		print("No power found. Assigning empty string.")
		power = ""

	type = getAttribute("type", html)
	if type is None:
		print("No type found. Assigning empty string.")
		type = ""

	race = getAttribute("race", html)
	if race is None:
		print("No race found. Not a creature? Card type is: " + type)
		race = ""

	effText = parseEffect(html)
	if effText == "":
		print("WARNING: Effect text not found! Vanilla card?")
	# else:
	# 	print("effect text is:\n"+effText)

	rarity = ""
	setNum = ""

	if setName == "":
		print("No set given. Assigning promo rarity")
		rarity = "Promo"
		setNum = "None"
	else:
		found = 0
		for i in range(1,100):
			setStr = "set"+ str(i)
			j = html.find(setStr)
			if j != -1:
				setNameToCheck = getAttribute(setStr, html).strip(" \n|")
				setNameToCheck = setNameToCheck.replace(" ","_")
				# print(setStr+" name is:"+setNameToCheck+" and set to match against is: "+setName)
				if(setName == setNameToCheck):
					rarity = getAttribute(" R"+str(i), html).strip(" \n|")
					print("Set match found!! Assigning rarity: "+rarity)
					setNum = getAttribute("setnum"+str(i), html).strip(" \n|")
					setNumList = setNum.split(", ")
					setNum = setNumList[0].strip(" ,")
					print("Assigning set number :"+setNum)
					if i > 1:
						print("INFO: Possible reprint.")
					found = 1
					break
		if found == 0:
			print("ERROR! No set found! Can't assign rarity and set number!")
	cardID = str(uuid.uuid4())

	cardName = cardName.replace("\"", "\'").replace("_", " ")
	cardXML = "\t\t<card name=\""+cardName+"\" id=\""+cardID+"\">\n"

	if "Dragheart Fortress" in type or "Field" or " Aura" in type:
		cardXML = cardXML.replace(">\n", "size=\"wide\">\n")

	cardXML = cardXML + makeXMLLine("Format", "OCG")
	cardXML = cardXML + makeXMLLine("Civilization", civ)
	cardXML = cardXML + makeXMLLine("Cost", cost)
	cardXML = cardXML + makeXMLLine("Type", type)
	cardXML = cardXML + makeXMLLine("Race", race)
	cardXML = cardXML + makeXMLLine("Power", power)
	cardXML = cardXML + makeXMLLine("Rules", effText)
	cardXML = cardXML + makeXMLLine("Rarity", rarity)
	cardXML = cardXML + makeXMLLine("Number", setNum)

	cardXML = cardXML + "\t\t</card>"

	#add condition for alternate and alternate2, and size
	return cardXML

def getAttribute(attr, html):
	i = html.lower().find(attr.lower()+" = ")
	if i < 0:
		return
	i += len(attr)+3
	j = html.find("\n", i)
	result = html[i:j] # got 'em
	# print(attr+" is: " + result)

	return result.strip()


def parseEffect(cardData):
	i = cardData.find('effect = ')
	if i == -1:
		return ""
	j = cardData.find('ocgeffect = ')
	effect = cardData[(i+9):j]
	effect = effect.strip("\n |")
	#print("Effect is :"+effect)

	effect = urllib.parse.quote(effect)

	with urllib.request.urlopen('https://duelmasters.fandom.com/api.php?action=parse&format=php&text='+effect) as response:
		html1 = response.read().decode('utf-8')

	html = ""
	html = str(html1)
	html = clean(html)
	return html

def clean(text):
	result = ""
	i = text.find("<p>") + 3
	j = text.rfind("</p>") - 1

	if i>0 and j>0:
		text = text[i:j]
	else:
		return "ERROR WITH PHP DATA, UNEXPECTED FORMAT"
	
	inTag = False
	i = 0

	while i < len(text):
		char = text[i]
		i += 1

		if char == '<':
			inTag = True

		if not inTag:
				result = result + char

		else:
			if char == '>':
				inTag = False

	result = result.replace('&#160;', '')
	result = result.replace('■', '>')
	result = result.replace('—', ' - ')
	result = result.replace(" \n", "\n")
	result = result.replace('\n', '&#xd;&#xa;')
	result = result.replace('> ', '')
	result = result.replace(".)", ")")
	result = result.replace(" (", "(")
	result = result.replace("\"", "\'")

	return result


def makeXMLLine(property, value):
	return "\t\t\t<property name=\""+property+"\" value=\""+value+"\" />\n"


# result = extractCardData(temp, temp2)
# print(result)
