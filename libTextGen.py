#!/usr/bin/env python3

import random


def genText(g):
    """
    Generate a valid text from a grammar

    Keyword arguments:
        g = grammar

    Return value:
        text = string representing the generated text
    """

    text = [ g['start'] ]                       # start with the starting variable
    while set(text).intersection(g['rnames']):  # while there are vars in the text
        newtext = []                            # use a temporary new list
        for symbol in text:                     # go through the current list
            if symbol in g['rnames']:           # if we see a variable
                prods = g['rules'][symbol]      # get its productions
                prod = random.choice(prods)     # randomly select one of them
                newtext.extend(prod)            # and add it to the temporary list
            else:                               # if it's not a variable
                newtext.append(symbol)          # just add it to the temporary list
        text = newtext                          # and the temporary list is now the current list

    return ' '.join(text)
