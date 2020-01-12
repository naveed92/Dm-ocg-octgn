from CardExtractor import *

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
	cardCount = 0

	for line in lines:
		i = line.find("[[")
		j = line.find("]]")

		if i > 0 and j > 0:
			i = i + 2
			cardName = line[i:j].replace(" ", "_")
			print(str(cardCount) + " Card is: "+ cardName)
			cardCount+= 1

			print(extractCardData(cardName))


extractSet(temp)
