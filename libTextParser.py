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

    d = [ [] for _ in t ]                               # d is a list of dsets: d[0], d[1], ..., d[len(t) - 1]
    d.append( [] )                                      # we need a d[len(t)] as well
    d[0] = expandFromGrammar(g, d[0], 0, g['start'])    # populate d[0] expanding the starting rule from the grammar

    # create d[n] for n = 1..len(t)
    for n, rsymbol in enumerate(t, start=1):    # loop through the words in the text counting them from 1
        for drule in d[n-1]:                    # look in the previous dset
            dot = drule['dot']
            if dot == drule['nsymbols']:        # this drule is already finished, skip it
                continue
            if drule['prod'][dot] == rsymbol:       # if this drule has the current word after the dot
                d[n] = advanceDot(g, drule, d, n)   # advance the dot and propagate this all around dn

    # to accept the text, we must have a drule in the last dset with:
    for drule in d[n]:
        if(drule['rname'] == g['start'] and         # rname as starting symbol,
           drule['dot'] == drule['nsymbols'] and    # the dot in the end of the production,
           drule['slash'] == 0):                    # and it must end with /0
            return True

    return False


def expandFromGrammar(g, dset, slash, s):
    rulestoproc = [s]       # vars to process
    rulesprocced = []       # vars already processed

    while rulestoproc != []:        # while there are rules to process
        rule = rulestoproc.pop(0)   # take the current rule
        rulesprocced.append(rule)   # list it as processed
        for prod in g['rules'][rule]:   # for each production
            drule = {                   # add this production in grammar format to d0 in d_rule format:
                'rname': rule,              # var name,
                'prod': prod,               # current production,
                'nsymbols': len(prod),      # number of symbols in the production,
                'dot': 0,                   # index of the string in the production that comes after the •,
                'slash': slash,             # and the immutable value of "/n"
            }
            dset.append(drule)
            dotsymbbol = prod[ drule['dot'] ]       # now take the symbol right after the dot
            if(dotsymbbol in g['rnames'] and        # if it's a variable
               not dotsymbbol in rulesprocced and   # not yet processed
               not dotsymbbol in rulestoproc):      # and not already listed to process
                rulestoproc.append(prod[0])         # list it to process

    return dset


def advanceDot(g, drule, d, n):
    """Copy a drule to the current dset advancing the dot and propagating to other drules"""

    newdrule = drule.copy() # do it this way, otherwise you're copying a pointer
    newdrule['dot'] += 1    # advance the dot
    d[n].append(newdrule)   # copy to the current dset

    if newdrule['dot'] == newdrule['nsymbols']:         # the dot reached the end of the drule
        slash = newdrule['slash']
        rname = newdrule['rname']
        d[n] = expandFromSlash(g, d, n, slash, rname)   # expand it from the slash dset
    else:
        nextsymbol = newdrule['prod'][ newdrule['dot'] ]
        if nextsymbol in g['rnames']:                           # the dot reached a variable
            d[n] = expandFromGrammar(g, d[n], n, nextsymbol)    # expand it from the grammar

    return d[n]


def expandFromSlash(g, d, n, slash, rname):
    """Copy to dn all the drules in d[slash] that had rname after the dot, advancing the dot"""

    for drule in d[slash]:                  # look in the slash dset
        dot = drule['dot']
        if dot == drule['nsymbols']:        # this drule is already finished, skip it
            continue
        if drule['prod'][dot] == rname:     # if this drule has the finished var after the dot
            advanceDot(g, drule, d, n)      # advance the dot and propagate this all around dn

    return d[n]