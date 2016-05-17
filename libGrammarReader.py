#!/usr/bin/env python3

import re


"""
Grammar type specifications:

grammar is a dictionary X => Y where
    X is 'terms', 'rnames', 'start' or 'rules'
    Y depends on the value of X:
    'terms' => Y is a set of strings representing terminal symbols
    'rnames' => Y is a set of strings representing variables
    'start' => Y is a string representing the starting variable
    'rules' => Y is a dictionary M => N where
        M is a string representing a variable name
        N is a list of tuples of strings representing productions for that variable
"""


class ParseError(Exception):
    """ParseError exception name declaration and messages"""
    termsMsg = 'Error parsing the terminals list!'
    rnamesMsg = 'Error parsing the variables list!'
    startMsg = 'Error parsing the starting variable!'
    rulesMsg = 'Error parsing the grammar rules!'
    pass


def parseGrammarFile(fname):
    """
    Open and parse a text file into a grammar type

    Keyword arguments:
        fname = string describing the name of the grammar file

    Return value:
        g = the interpreted grammar in grammar format
    """

    # if anything goes wrong, skip the rest of the block
    # to know more, search for 'python exception handling'
    try:
        fp = open(fname, 'r')

        g = {
            'terms': [],    # list of terminals
            'rnames': [],   # list of variables
            'start': "",    # starting symbol
            'rules': {},    # rnames and their lists of productions
        }

        g['terms'] = parseTerms(fp)
        g['rnames'] = parseVars(fp)
        g['start'] = parseStart(fp)
        g['rules'] = parseRules(fp)

        fp.close()
        return g

    # TODO: this must go on __main__
    except ParseError as error:
        print(error.args[0])
        exit(-1)

    # re-raise the rest of exceptions to __main__
    except:
        raise


def parseTerms(fp):
    """
    Parse lines from a text file into the set of grammar terminals

    Keyword arguments:
        fp = handle to the open grammar file

    Return value:
        set containing the list of terminal strings
    """

    try:
        # match "Terminais", with or without a comment etc., using RegEx
        # to know more, search for 'python regular expressions'
        ln = fp.readline()
        p = re.compile(r'^Terminais\s*(?:#.*)?$')
        m = p.match(ln)
        if m == None:
            raise ParseError(ParseError.termsMsg)

        # match and capture "{ a, b }" etc.
        ln = fp.readline()
        p = re.compile(r'^\{\s*(.*)\s*\}\s*(?:#.*)?$')
        m = p.match(ln)
        if m == None:
            raise ParseError(ParseError.termsMsg)

        # split the string by ',', trim spaces and return as a set
        a = m.group(1).split(',')   # group(1) contains each captured group
        a[:] = map(str.strip, a)    # trim spaces in each element of a
        return set(a)               # remove duplicates

    except:
        # re-raise the exception to handle it in the caller
        raise


def parseVars(fp):
    """
    Parse lines from a text file into the set of grammar variables

    Keyword arguments:
        fp = handle to the open grammar file

    Return value:
        set containing the list of variable names
    """

    try:
        ln = fp.readline()
        p = re.compile(r'^Variaveis\s*(?:#.*)?$')
        m = p.match(ln)
        if m == None:
            raise ParseError(ParseError.rnamesMsg)

        ln = fp.readline()
        p = re.compile(r'^\{\s*(.*)\s*\}\s*(?:#.*)?$')
        m = p.match(ln)
        if m == None:
            raise ParseError(ParseError.rnamesMsg)

        a = m.group(1).split(',')
        a[:] = map(str.strip, a)
        return set(a)

    except:
        raise


def parseStart(fp):
    """
    Parse lines from a text file into the starting variable

    Keyword arguments:
        fp = handle to the open grammar file

    Return value:
        string representing the starting variable name
    """

    try:
        ln = fp.readline()
        p = re.compile(r'^Inicial\s*(?:#.*)?$')
        m = p.match(ln)
        if m == None:
            raise ParseError(ParseError.startMsg)

        # match and capture "{ a }" etc.
        ln = fp.readline()
        p = re.compile(r'^\{\s*(.*)\s*\}\s*(?:#.*)?$')
        m = p.match(ln)
        if m == None:
            raise ParseError(ParseError.startMsg)

        return m.group(1).strip()

    except:
        raise


def parseRules(fp):
    """
    Parse lines from a text file into the grammar rules

    Keyword arguments:
        fp = handle to the open grammar file

    Return value:
        rules = dictionary with variable names and their productions
    """

    try:
        ln = fp.readline()
        p = re.compile(r'^Regras\s*(?:#.*)?$')
        m = p.match(ln)
        if m == None:
            raise ParseError(ParseError.rulesMsg)

        rules = {}

        # process each line until the end
        for line in fp:
            # skip empty lines
            if len(line) < 3:   # expect at least "{>}"
                continue
            
            # match "{ a > a, b }" etc.
            p = re.compile(r'^\{\s*(.*)\s*>\s*(.*)\s*\}\s*;?\s*(?:#.*)?$')
            m = p.match(line)
            if m == None:
                raise ParseError(ParseError.rulesMsg)

            rname = m.group(1).strip()      # group(1) = rname
            prods = m.group(2).split(',')   # group(2) = productions string
            prods[:] = map(str.strip, prods)
            prods = tuple(prods)            # convert it to a tuple (immutable list)

            # add each production to dict['variable']
            if not rname in rules.keys():   # create a new dict entry?
                rules[rname] = []
            rules[rname].append(prods)
            
        # remove duplicate productions
        for rname in rules.keys():
            rules[rname] = list(set(rules[rname]))

        return rules

    except:
        raise
