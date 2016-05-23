#!/usr/bin/env python3

import copy
from libExcept import *


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
    'hist' => Y is a list of drules corresponding to the expanded variables of the production
"""


def parseText(g, text):
    """
    Determine whether or not a text can be produced by a grammar, using the Earley algorithm

    Keyword arguments:
        g = grammar
        text = string to be parsed

    Return value:
        bool = whether or not text was accepted as a sentence of g
        str = derivation tree(s) if accepted
    """

    if not g:
        raise GrammarError()

    t = text.split()
    t[:] = map(str.strip, t)    # strip spaces from each word in the text
    if len(t) == 0:
        return False, ""

    d = [ [] for _ in t ]                               # d is a list of dsets: d[0], d[1], ..., d[len(t) - 1]
    d.append( [] )                                      # we need a d[len(t)] as well
    d[0] = expandFromGrammar(g, d[0], 0, g['start'])    # populate d[0] expanding the starting rule from the grammar

    # create d[n] for n = 1..len(t)
    for n, rsymbol in enumerate(t, start=1):    # loop through the words in the text counting them from 1
        for drule in d[n-1]:                    # look in the previous dset
            dot = drule['dot']
            if dot == drule['nsymbols']:        # this drule is already finished, skip it
                continue
            if drule['prod'][dot] == rsymbol:               # if this drule has the current word after the dot
                d[n] = advanceDot(g, drule, d, n, rsymbol)  # advance the dot and propagate this all around dn

    # to accept the text, we must have a drule in the last dset with:
    accepts = []
    for drule in d[n]:
        if(drule['rname'] == g['start'] and         # rname as starting symbol,
           drule['dot'] == drule['nsymbols'] and    # the dot in the end of the production,
           drule['slash'] == 0):                    # and it must end with /0
            accepts.append(drule)
    if len(accepts) > 0:        # we may have more than one tree
        strtrees = generateAllTrees(accepts)
        return True, strtrees
    else:
        return False, ""


def expandFromGrammar(g, dset, slash, s):
    """
    Expand a drule from the grammar in the current dset

    Keyword arguments:
        g = grammar
        dset = list of drules
        slash = integer describing a dset index
        s = string describing the first variable to be expanded

    Return value:
        dset = new dset after expanding from the grammar
    """

    rulestoproc = [s]   # vars to process
    rulesprocced = []   # vars already processed

    while rulestoproc != []:        # while there are rules to process
        rule = rulestoproc.pop(0)   # take the current rule
        rulesprocced.append(rule)   # list it as processed
        for prod in g['rules'][rule]:   # for each production
            drule = {                   # add this production in grammar format to d0 in drule format:
                'rname': rule,              # var name,
                'prod': prod,               # current production,
                'nsymbols': len(prod),      # number of symbols in the production,
                'dot': 0,                   # index of the string in the production that comes after the dot,
                'slash': slash,             # the immutable value of "/n"
                'hist': [],                 # and the empty list of generated drule "pointers"
            }
            if not drule in dset:
                dset.append(drule)
            dotsymbbol = prod[ drule['dot'] ]       # now take the symbol right after the dot
            if(dotsymbbol in g['rnames'] and        # if it's a variable
               not dotsymbbol in rulesprocced and   # not yet processed
               not dotsymbbol in rulestoproc):      # and not already listed to process
                rulestoproc.append(prod[0])         # list it to process

    return dset


def advanceDot(g, drule, d, n, hist):
    """
    Copy a drule to the current dset advancing the dot and propagating to other drules

    Keyword arguments:
        g = grammar
        drule = dictionary describing a rule in a dset
        d = list of dsets
        n = integer describing a dset index
        hist = drule or string that caused the dot to advance

    Return value:
        d[n] = new dset after advancing the dot and propagating to the other rules
    """

    newdrule = copy.deepcopy(drule)     # do it this way, otherwise you're making a shallow copy
    newdrule['dot'] += 1                # advance the dot
    newdrule['hist'].append(hist)       # add the generating rule to the history

    if not newdrule in d[n]:
        d[n].append(newdrule)   # copy to the current dset

    if newdrule['dot'] == newdrule['nsymbols']:         # the dot reached the end of the drule
        d[n] = expandFromSlash(g, d, n, newdrule)       # expand it from the slash dset
    else:
        nextsymbol = newdrule['prod'][ newdrule['dot'] ]
        if nextsymbol in g['rnames']:                           # the dot reached a variable
            d[n] = expandFromGrammar(g, d[n], n, nextsymbol)    # expand it from the grammar

    return d[n]


def expandFromSlash(g, d, n, newdrule):
    """
    Copy to dn all the drules in d[slash] that had rname after the dot, advancing the dot

    Keyword arguments:
        g = grammar
        d = list of dsets
        n = integer describing a dset index
        newdrule = dictionary describing a generating rule in a dset

    Return value:
        d[n] = new dset after advancing the dot and propagating to the other rules
    """

    newslash = newdrule['slash']
    newrname = newdrule['rname']
    for drule in d[newslash]:                           # look in the slash dset
        dot = drule['dot']
        if dot == drule['nsymbols']:                    # this drule is already finished, skip it
            continue
        if drule['prod'][dot] == newrname:              # if this drule has the finished var after the dot
            d[n] = advanceDot(g, drule, d, n, newdrule) # advance the dot and propagate this all around dn

    return d[n]


def generateAllTrees(accepts):
    """
    Generate all the derivation trees for the accepted drules

    Keyword arguments:
        accepts = set of all the drules accepted by parseText

    Return value:
        str = string with all the derivation trees
    """

    strtrees = ""
    if len(accepts) > 1:                                # we may have more than one tree
        for n, drule in enumerate(accepts, start=1):
            strtrees +="\n\nTree no. " + str(n) + ":\n"   # generate them all, numbered
            strtrees += generateTree(drule, 0)
    else:
        strtrees +="\n\nTree:\n"
        for drule in accepts:
            strtrees += generateTree(drule, 0)          # otherwise, generate just this one

    return strtrees


def generateTree(drule, indent):
    """
    Generate a derivation tree for the accepted drule

    Keyword arguments:
        drule = dictionary describing a rule in a dset
        indent = integer used to indent the output

    Return value:
        str = string with all the derivation trees
    """

    strtree = indent*4*' ' + drule['rname']                 # concatenate the rname
    for item in drule['hist']:                              # go through this rule's history
        if isinstance(item, str):                           # test if it's a string
            strtree += '\n' + (indent+1)*4*' ' + item       # if it is, just concatenate
        else:
            strtree += '\n' + generateTree(item, indent+1)  # else, start a higher-level recursion

    return strtree
