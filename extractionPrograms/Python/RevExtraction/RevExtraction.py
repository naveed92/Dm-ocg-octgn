from CardExtractor import *

temp = "Dogiragon,_Flaming_Revolution"


result = extractCardData(temp)
print(result)

effText = parseEffect(result)
effText = effText.replace('\\\\', '\\')
effText = effText.replace('\\\\', '\\')
effText = effText.replace('&#160;', '')
effText = effText.replace('\\xe2\\x96\\xa0', '>')
effText = effText.replace('\\xe2\\x80\\x94', ' - ')
effText = effText.replace('\\n', '&#xd;&#xa;')
effText = effText.replace('\\\'', '\'')
effText = effText.replace('> ', '')
effText = effText[0:-1]
print (effText)

