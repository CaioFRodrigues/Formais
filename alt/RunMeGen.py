#!/usr/bin/env python3

import os, sys
from libGrammarReader import parseGrammarFile
from libTextGen import genText


if len(sys.argv) != 2:
    print("Usage: %s gramatica.txt" % os.path.basename(sys.argv[0]))
    exit(1)

g = parseGrammarFile(sys.argv[1])
text = genText(g)
print(text)