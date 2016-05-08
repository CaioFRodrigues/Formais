#!/usr/bin/env python3

from libGrammarReader import *


"""
d and dset type specifications:

d is a list of dsets referenced by a number starting in 0

a dset is a list of drules

a drule is a dictionary X => Y where
    X is 'rname', 'prod', 'nsymbols', 'dot' or 'slash'
    Y depends on the value of X:
    'rname' => Y is a string representing the name of the variable
    'prod' => Y is a set of strings representing a production for that variable
    'nsymbols' => Y is an int representing the number of symbols in the production
    'dot' => Y is an int representing the position of the dot in the production
    'slash' => Y is an int representing the value of the '/n' in the end of the drule
"""


def parseText(g, text):
    """Determine whether or not a text can be produced by a grammar, using the Earley algorithm"""

    t = text.split()
    t[:] = map(str.strip, t)    # strip spaces from each word in the text

    d = [ [] for _ in t ]       # d is a list of dsets: d[0], d[1], ..., d[len(t)]
    d[0] = createD0(g)          # populate d[0]

    # TODO: split this into more functions
    # it's currently ugly af
    for n, rsymbol in enumerate(t, start=1):    # loop through the words in the text counting them from 1
        for drule in d[n-1]:                    # look in the last dset
            dot = drule['dot']
            if dot == drule['nsymbols']:        # this drule is already over, skip it
                continue
            if drule['prod'][dot] == rsymbol:   # if this drule has the current word after the dot
                newdrule = drule.copy()
                newdrule['dot'] += 1
                d[n].append(newdrule)           # copy it to the new dset, advancing the dot
                if newdrule['dot'] == newdrule['nsymbols']:     # the dot reached the end of the drule
                    slash = newdrule['slash']
                    '''
                    Expande do conjunto ['slash'] as regras que têm ['rname'] no índice ['dot'], avançando o ['dot']
                    '''
                    pass
                else:
                    nextsymbol = newdrule['prods'][ newdrule['dot'] ]
                    if nextsymbol in g['rnames']:   # the dot reached a variable that needs expansion from g
                        '''
                        Expande ela da gramática com ['dot'] = 0 e ['slash'] = n
                        '''
                        pass

    # to accept the text, we must have a drule with
    for drule in d[n-1]:
        if(drule['rname'] == g['start'] and         # rname = starting symbol,
           drule['dot'] == drule['nsymbols'] and    # the dot in the end of the production,
           drule['slash'] == 0):                    # and it must end with /0
            return True

    return False


def createD0(g):
    """Create the first set of drules: D0"""

    d0 = []
    rulestoproc = [g['start']]  # vars to process, starting on the starting symbol
    rulesprocced = []           # vars already processed

    while rulestoproc != []:        # while there are rules to process
        rule = rulestoproc.pop(0)   # take the current rule
        rulesprocced.append(rule)   # list it as processed
        for prod in g['rules'][rule]:   # for each production
            drule = {                   # add this production in grammar format to d0 in d_rule format:
                'rname': rule,              # var name,
                'prod': prod,               # current production,
                'nsymbols': len(prod),      # number of symbols in the production,
                'dot': 0,                   # index of the string in the production that comes after the •,
                'slash': 0,                 # and the immutable value of "/n"
            }
            d0.append(drule)
            dotsymbbol = prod[ drule['dot'] ]           # now take the symbol right after the dot
            if(dotsymbbol in g['rnames'] and            # if it's a variable
               not dotsymbbol in rulesprocced and       # not yet processed
               not dotsymbbol in rulestoproc):          # and not already listed to process
                rulestoproc.append(prod[0])             # list it to process

    return d0