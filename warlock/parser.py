#!/usr/bin/env python3
import sys
from parsimonious.grammar import Grammar


WARLOCK_GRAMMAR = Grammar(
    r"""
    program = newline? exprs newline?
    exprs = expr (newline expr)*
    expr = !reserved (statement / literal / funcall / symbol)

    reserved = "INDENT" / "DEDENT"

    newline = ~r"\n+"
    ws = ~r"\s+"

    statement = if_stmt_group / for_stmt / while_stmt / function_def / return_stmt / assignment
    if_stmt_group = if_stmt elif_stmt* else_stmt?
    if_stmt = "if" ws expr ":" newline block
    elif_stmt = "el" if_stmt
    else_stmt = "else:" newline block
    for_stmt = "for" ws symbol ws "in" ws expr ":" newline block
    while_stmt = "while" ws expr ":" newline block
    function_def = "def" ws symbol ws? "(" (ws? expr (ws? "," ws? expr)*)? ws? "):" newline block
    return_stmt = "return" ws
    assignment = symbol ws? "=" ws? expr
    block = "INDENT" newline exprs newline "DEDENT"

    funcall = symbol ws? "(" ws? (expr ("," ws expr)*)? ws? ")"

    literal = integer / string
    string = "\"" ~r"[^\"]*" "\""
    integer = ~r"[0-9]+"

    symbol = ~r"[A-Z0-9][A-Z0-9-_]*"i
    """)


def parse(program):
    return WARLOCK_GRAMMAR.parse(program)


if __name__ == "__main__":
    print(WARLOCK_GRAMMAR.parse(sys.stdin.read()))
