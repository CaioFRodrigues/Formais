from libGrammarReader import parseGrammarFile
from libTextGen import genText

# func to send the text to the GUI

def RunMeGenFunc():
    g = parseGrammarFile("gramatica.txt")
    text = genText(g)
    return text