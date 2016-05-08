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

g = parseGrammarFile(sys.argv[1])

d = []                      # d is a list of d0, d1, ...
rulestoproc = [g['start']]  # vars to process, starting on the starting symbol
rulesprocced = []           # vars already processed

# create d0
d.append([])
while rulestoproc != []:        # while there are rules to process
    rule = rulestoproc.pop(0)   # take the current rule
    rulesprocced.append(rule)   # list it as processed
    for prod in g['rules'][rule]:   # for each production
        drule = {                   # add this production in grammar format to d0 in d_rule format
            'rname': rule,          # var name
            'prod': prod,           # current production
            'nsymbols': len(prod),  # number of symbols in the production
            'dot': 0,               # index of the string in the production that comes after the •
            'slash': 0,             # the immutable value of "/n"
        }
        d[0].append(drule)
        dotsymbbol = prod[ drule['dot'] ]       # now take the symbol right after the dot
        if ( dotsymbbol in g['rnames'] and      # if it's a variable
             not dotsymbbol in rulesprocced and # not yet processed
             not dotsymbbol in rulestoproc ):   # and not already listed to process
            rulestoproc.append(prod[0])         # list it to process


# print d0
print("d0:")
for drule in d[0]:
    print("{ %s > %s }; nsymbols=%d; dot=%d; slash=%d" % (
        drule['rname'], ', '.join(drule['prod']), drule['nsymbols'], drule['dot'], drule['slash']))