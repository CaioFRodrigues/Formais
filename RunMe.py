#!/usr/bin/env python3

import os, sys
from libGrammarReader import *


if len(sys.argv) != 2:
    print("Usage: %s gramatica.txt" % os.path.basename(sys.argv[0]))
    exit(1)

g = parseGrammarFile(sys.argv[1])
print('terms:')
print(g['terms'])
print('vars:')
print(g['vars'])
print('start:')
print(g['start'])
print('rules:')
for var in g['rules']:
    for prods in g['rules'][var]:
        print(var + ' > ' + ', '.join(prods))
