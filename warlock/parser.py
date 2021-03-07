#!/usr/bin/env python3
import sys
from parsimonious.grammar import Grammar


# WARLOCK_GRAMMAR = Grammar(
#     """
#     newline = "\n"
#     indent = "INDENT"
#     dedent = "DEDENT"
#     func_name = ~r"[a-zA-Z]\S*"
#     single_quoted_string_literal = "'" ~r"[^']" "'"
#     double_quoted_string_literal = "\"" ~r"[^\"]" "\""
#     string_literal = single_quoted_string_literal | double_quoted_string_literal
#     func_call = func_name "(" (string_literal ("," string_literal)*)? ")"
#     func_def = "def" " " func_name "():" newline indent newline expr (newline expr)* newline dedent
#     expr = func_def | func_call
#     program = (expr (newline expr)*)?
#     """)

SIMPLE_GRAMMAR = Grammar(
    r"""
    program = (expr newline* (newline+ expr)*)?
    newline = "\n"
    expr = literal / funcall / symbol

    ws = ~r"\s+"

    funcall = symbol ws? "(" ws? (expr ("," ws expr)*)? ws? ")"

    literal = integer / string
    string = "\"" ~r"[^\"]*" "\""
    integer = ~r"[0-9]+"

    symbol = ~r"[A-Z0-9][A-Z0-9-_]*"i
    """)


def parse(program):
    return SIMPLE_GRAMMAR.parse(program)


if __name__ == "__main__":
    print(SIMPLE_GRAMMAR.parse(sys.stdin.read()))
