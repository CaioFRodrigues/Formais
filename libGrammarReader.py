#!/usr/bin/env python3

import re


"""
Grammar type specifications:

grammar is a dictionary X => Y where
    X is 'terms', 'vars', 'start' or 'rules'
    Y depends on the value of X:
    'terms' => Y is a list of strings representing terminal symbols
    'vars' => Y is a list of strings representing variables
    'start' => Y is a string representing the starting variable
    'rules' => Y is a dictionary M => N where
        M is a string representing a variable name
        N is a list of strings representing productions for that variable
"""


class ParseError(Exception):
    """ParseError exception name declaration and messages"""
    termsMsg = 'Error parsing the terminals list!'
    varsMsg = 'Error parsing the variables list!'
    startMsg = 'Error parsing the starting variable!'
    rulesMsg = 'Error parsing the grammar rules!'
    pass


def parseGrammarFile(fname):
    """Open and parse a text file into a grammar type"""

    # if anything goes wrong, skip the rest of the block
    # to know more, search for 'python exception handling'
    try:
        fp = open(fname, 'r')

        grammar = {
            'terms': [],    # list of terminals
            'vars': [],     # list of variables
            'start': "",    # starting symbol
            'rules': {},    # vars and their lists of productions
        }

        grammar['terms'] = parseTerms(fp)
        grammar['vars'] = parseVars(fp)
        grammar['start'] = parseStart(fp)
        grammar['rules'] = parseRules(fp)

        fp.close()
        return grammar

    # treat specific exceptions
    except FileNotFoundError:
        print('File not found!')
        exit(-1)

    except ParseError as error:
        print(error.args[0])
        exit(-1)

    # treat the rest of exceptions
    except:
        print('Unknown error!')
        exit(-1)


def parseTerms(fp):
    """Parse lines from a text file into the list of grammar terminals"""

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

        # split the string by ',', trim spaces and return as a list
        a = m.group(1).split(',')   # group(1) contains each captured group
        a[:] = map(str.strip, a)    # trim spaces
        return a

    except:
        # re-raise the exception to handle it in the caller
        raise


def parseVars(fp):
    """Parse lines from a text file into the list of grammar variables"""

    try:
        ln = fp.readline()
        p = re.compile(r'^Variaveis\s*(?:#.*)?$')
        m = p.match(ln)
        if m == None:
            raise ParseError(ParseError.varsMsg)

        ln = fp.readline()
        p = re.compile(r'^\{\s*(.*)\s*\}\s*(?:#.*)?$')
        m = p.match(ln)
        if m == None:
            raise ParseError(ParseError.varsMsg)

        a = m.group(1).split(',')
        a[:] = map(str.strip, a)
        return a

    except:
        raise


def parseStart(fp):
    """Parse lines from a text file into the starting variable"""

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
    """Parse lines from a text file into the grammar rules"""

    try:
        ln = fp.readline()
        p = re.compile(r'^Regras\s*(?:#.*)?$')
        m = p.match(ln)
        if m == None:
            raise ParseError(ParseError.rulesMsg)

        rules = {}

        # process each line until the end
        for line in fp:
            # match "{ a > a, b }" etc.
            p = re.compile(r'^\{\s*(.*)\s*>\s*(.*)\s*\}\s*;?\s*(?:#.*)?$')
            m = p.match(line)
            if m == None:
                raise ParseError(ParseError.rulesMsg)

            var = m.group(1).strip()        # group(1) = var
            prods = m.group(2).split(',')   # group(2) = productions string
            prods[:] = map(str.strip, prods)

            # add each production to dict['variable']
            if not var in rules.keys():     # create a new dict entry?
                rules[var] = []
            rules[var].append(prods)

        return rules

    except:
        raise
