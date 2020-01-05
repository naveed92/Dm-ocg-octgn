import urllib.request
import urllib.parse
import re

def extractCardData(cardName):
	with urllib.request.urlopen('https://duelmasters.fandom.com/api.php?action=query&prop=revisions&rvprop=content&format=php&titles='+cardName) as response:
		html1 = response.read()

	html=""
	html = str(html1)

	i = html.find('{{Cardtable') +26
	j = html.find('ocgeffect')
	if j == -1:		##Vanilla card
		j = html.find('flavor')
		if j == -1:
			j = html.find('artist')

	j-=1

	html = html[i:j]
	html = html.replace('\\n','\n')

	return(html)

def parseEffect(cardData):
	i = cardData.find('effect = ')
	if i == -1:
		print("No effect! Vanilla card?")
		return
	effect = cardData[(i+9):-1]
	print("Effect is :"+effect)

	effect = urllib.parse.quote(effect)

	with urllib.request.urlopen('https://duelmasters.fandom.com/api.php?action=parse&format=php&text='+effect) as response:
		html1 = response.read()

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
