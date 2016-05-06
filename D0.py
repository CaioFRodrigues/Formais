#!/usr/bin/env python3

import os, sys
from libGrammarReader import *


if len(sys.argv) != 3:
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

'''

''' 
S -> [NP, PP] {2, 0} # nsymbols, dot

NP -> .NP VP
NP -> .VP VP
VP -> .the

'''

'''
Cattani, por favor, pare de usar classes
Assim fica mais c00l
Ass: Class Grupo:
			__init__(foda-se) xD
'''

d = [[]]

rulestoproc = [g['start']]
rulesprocced = []

while rulestoproc:	# while there are rules to process
	rule = rulestoproc.pop(0)
	rulesprocced.append(rule)
	print(rule)
	for prod in g['rules'][rule]:
		d[0].append({
			'rname': rule,
			'prod': prod,
			'nsymbols': len(prod),
			'dot': 0,
			'slash': 0,
		})
		print("\t%s" % prod)
		if not prod[0] in rulesprocced and not prod[0] in g['terms']:	# if the symbol immediately after the dot is not yet processed
			rulestoproc.append(prod[0])


