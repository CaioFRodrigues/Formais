#!/usr/bin/env python3

# import os, sys
from libGrammarReader import parseGrammarFile
from libTextParser import parseText

# main function created from RunMeParser
# uses as parameter:
#   text -> aux string
def RunMeParserFunc(text, filePath):
    # if len(sys.argv) != 3:
    #     print("Usage: %s gramatica.txt \"text to parse\" " % os.path.basename(sys.argv[0]))
    #     exit(1)

    g = parseGrammarFile(filePath)
    acc, trees = parseText(g, text)

    if acc:
        return 'Text accepted!' + trees
    else:
        return 'Text rejected!'