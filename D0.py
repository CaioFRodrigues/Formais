#!/usr/bin/env python3

import os, sys
from libGrammarReader import *


if len(sys.argv) != 2:
    print("Usage: %s gramatica.txt" % os.path.basename(sys.argv[0]))
    exit(1)


'''
_AD_ > .NP PP /0
NP > .A BC /0
A > .the /0
'''

'''
d[0] => [
			{rname (string), prod (list of strings), nsymbols (int), dot (int), slash (int)},
			{rname (string), prod (list of strings), nsymbols (int), dot (int), slash (int)},
			{rname (string), prod (list of strings), nsymbols (int), dot (int), slash (int)},
			{rname (string), prod (list of strings), nsymbols (int), dot (int), slash (int)},
		]

d0 é uma lista de dicionários, onde cada um é como tá aí em cima
'''

''' 
S > [NP, PP] {2, 0} # nsymbols, dot

NP > .NP VP ==> {rname: 'NP', prod: ['NP', 'VP'], nsymbols: 2, dot: 0, slash: 0}
NP > .VP VP ==> {rname: 'NP', prod: ['VP', 'VP'], nsymbols: 2, dot: 0, slash: 0}
VP > .the   ==> {rname: 'VP', prod: ['the'], nsymbols: 1, dot: 0, slash: 0}

'''

'''
Cattani, por favor, pare de usar classes
Assim fica mais c00l
Ass: Class Grupo:
			__init__(foda-se) xD
'''

d = [[]]                    # d is a list of d0, d1, ...
rulestoproc = [g['start']]  # vars to process, starting on the starting symbol
rulesprocced = []           # vars already processed

while rulestoproc != []:        # while there are rules to process
	rule = rulestoproc.pop(0)   # take the current rule
	rulesprocced.append(rule)   # list it as processed
	print(rule)
	for prod in g['rules'][rule]:   # for each production
        drule = {                   # add this production in grammar format to d0 in d_rule format
			'rname': rule,          # var name
			'prod': prod,           # current production
			'nsymbols': len(prod),  # number of symbols in the production
			'dot': 0,               # index of the string in the production that comes after the •
			'slash': 0,             # the immutable value of "/n"
		}
		d[0].append(drule)
		print(drule)
        dotsymbbol = prod[ drule['dot'] ]
		if not dotsymbbol in rulesprocced   # if the symbol after the dot is not yet processed
           and dotsymbbol in g['rnames']:   # and it's a variable
			rulestoproc.append(prod[0])     # process it ASAP


