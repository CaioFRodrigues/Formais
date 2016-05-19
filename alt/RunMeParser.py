#!/usr/bin/env python3

import os, sys
from libGrammarReader import parseGrammarFile
from libTextParser import parseText


if len(sys.argv) != 3:
    print("Usage: %s gramatica.txt \"text to parse\" " % os.path.basename(sys.argv[0]))
    exit(1)

g = parseGrammarFile(sys.argv[1])
acc, trees = parseText(g, sys.argv[2])

if acc:
    print('Text accepted!' + trees)
else:
    print('Text rejected!')
