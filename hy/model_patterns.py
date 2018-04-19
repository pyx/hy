# Copyright 2018 the authors.
# This file is part of Hy, which is free software licensed under the Expat
# license. See the LICENSE.

from hy.models import HyExpression, HySymbol, HyKeyword, HyString, HyList
from funcparserlib.parser import some, skip, many, finished, a
from functools import reduce
from operator import add

EXPR = some(lambda _: True)
SYM = some(lambda x: isinstance(x, HySymbol))
STR = some(lambda x: isinstance(x, HyString))

def sym(wanted):
    if wanted.startswith(":"):
        return skip(a(HyKeyword(wanted[1:])))
    return skip(some(lambda x: isinstance(x, HySymbol) and x == wanted))

def whole(parsers):
    if len(parsers) == 0:
        return finished >> (lambda x: [])
    if len(parsers) == 1:
        return parsers[0] + finished >> (lambda x: x[:-1])
    return reduce(add, parsers) + skip(finished)

def _grouped(group_type, parsers): return (
    some(lambda x: isinstance(x, group_type)) >>
    (lambda x: group_type(whole(parsers).parse(x)).replace(x, recursive=False)))

def sb(*parsers):
    return _grouped(HyList, parsers)

def form(*parsers):
    return _grouped(HyExpression, parsers)

def dolike(head):
    return form(sym(head), many(EXPR))

def notform(*disallowed_heads):
    return some(lambda x: not (
        isinstance(x, HyExpression) and
        x and
        isinstance(x[0], HySymbol) and
        x[0] in disallowed_heads))
