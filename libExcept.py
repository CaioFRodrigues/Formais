#!/usr/bin/env python3


class ParseError(Exception):
    """ParseError exception name declaration and messages"""
    termsMsg = 'Error parsing the terminals list!'
    rnamesMsg = 'Error parsing the variables list!'
    startMsg = 'Error parsing the starting variable!'
    rulesMsg = 'Error parsing the grammar rules!'
    pass


class GrammarError:
    """GrammarError exception name declaration"""
    pass
