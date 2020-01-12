import urllib.request
import urllib.parse


temp = "Smith, Breaking Right"

def extractCardData(cardName):
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

	print("Point 1, HTML is :\n"+html)

	##### Getting all the data #######
	#image can be gotten through query, check the other program with Yomi
	name = cardName.replace("_", " ")

	cost = getAttribute("cost", html)
	if cost is None:
		print("ERROR: No cost found!")

	civ = getAttribute("civilization", html)
	if civ is None:
		print("WARNING: No civ found! Assigning Zero.")
		civ = "Zero"

	race = getAttribute("race", html)
	if race is None:
		print("No race found. Not a creature?")

	power = getAttribute("power", html)
	if power is None:
		print("No power found. Assigning 0.")
		power = "0"


	return(html)

def getAttribute(attr, html):
	i = html.lower().find(attr.lower()+" = ")
	if i < 0:
		print("ERROR FINDING "+attr)
		return
	i += len(attr)+3
	j = html.find("\n", i)
	result = html[i:j] # got 'em
	print(attr+" is: " + result)

	return result


def parseEffect(cardData):
	i = cardData.find('effect = ')
	if i == -1:
		print("No effect! Vanilla card?")
		return ""
	effect = cardData[(i+9):-1]
	print("Effect is :"+effect)

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
		
	return result




result = extractCardData(temp)
#print(result)
effText = parseEffect(result)
effText = effText.replace('&#160;', '')
effText = effText.replace('■', '>')
effText = effText.replace('—', ' - ')
effText = effText.replace(" \n", "\n" )
effText = effText.replace('\n', '&#xd;&#xa;')
effText = effText.replace('> ', '')
effText = effText.replace(".)", ")")
effText = effText.replace(" (", "(")
effText = effText.replace("\"", "\'")
print(effText)
