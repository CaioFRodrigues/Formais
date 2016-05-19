from libGrammarReader import parseGrammarFile
from libTextGen import genText

# func to send the text to the GUI

def RunMeGenFunc(filePath):
    g = parseGrammarFile(filePath)
    text = genText(g)
    return text