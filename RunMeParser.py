#!/usr/bin/env python3

import os, sys
from libGrammarReader import *


if len(sys.argv) != 3:
    print("Usage: %s gramatica.txt \"the cat ate the dog\" " % os.path.basename(sys.argv[0]))
    exit(1)

g = parseGrammarFile(sys.argv[1])
""""print('terms:')
print(g['terms'])
print('vars:')
print(g['vars'])
print('start:')
print(g['start'])
print('rules:')
for var in g['rules']:
    for prods in g['rules'][var]:
        print(var + ' > ' + ', '.join(prods))
		
if (os.path.basename(sys.argv[2])):
	print(os.path.basename(sys.argv[2]))""" #original do RunMe.py

class parserCursor:

	def __init__(self, rules, cursor):
		self.rules = rules #2darray
		self.cursor = cursor #int

m = os.path.basename(sys.argv[2]).split(' ')
print (m) #frase que vem do argumento
print (m[0]) #primeira palavra do argumento

aux1 = 0
aux2 = 0
for var in g['rules']: #percorre dicionario do rules
	if var == g['start']: #acha o start
		rules = [[],[]] #cria o array 2d
		start = parserCursor(rules,0) #usa a classe que vai ter o cursor
		for prods in g['rules'][var]:
			start.rules[0].append(prods) #bota as producoes nele
			print(start.rules[0][0][0]) #extrai D0,primeira regra, primeira variável DEBUG
			
			