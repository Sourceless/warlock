#!/usr/bin/env python3
import sys
from parsimonious.grammar import Grammar


WARLOCK_GRAMMAR = Grammar(
    r"""
    program = newline? lines newline?
    lines = line (newline line)*
    line = comment / expr
    expr = infix_expr / lone_expr
    lone_expr = statement / call / literal / symbol
    infix_expr = lone_expr ws infix_identifier_inner ws expr
    comment = "#" ~r".*"

    reserved = "INDENT" / "DEDENT" / "define" / "let" / "fn"

    newline = ~r"\n+"
    ws = ~r" +"
    block = "INDENT" newline lines newline "DEDENT"
    args = "(" ws? (expr ("," ws expr)*)? ws? ")"

    statement = define / let / lambda / macro

    define = "define" ws symbol ws expr
    let = "let" ws symbol ws expr
    lambda = "fn" ws identifier (ws? "," ws? identifier)* ":" ((ws expr) / (newline block))
    call = symbol ws? args

    macro = stick_macro / block_macro_bare / block_macro_call / block_macro_args
    stick_macro = symbol "!" ws expr (ws expr)*
    block_macro_bare = symbol ":" newline block
    block_macro_args = symbol ws args ":" newline block
    block_macro_call = symbol ws symbol ws? args ":" newline block

    literal = integer / string
    string = "\"" ~r"[^\"]*" "\""
    integer = "-"? natural
    natural = ~r"[0-9]+"

    symbol = !reserved (identifier / infix_identifier)
    identifier = ~r"[A-Z0-9][A-Z0-9-_]*"i
    infix_identifier = "(" infix_identifier_inner ")"
    infix_identifier_inner = ~r"[+=-~<>/*$%!&_\\\.?@:;|]+"
    """)

def parse(program):
    return WARLOCK_GRAMMAR.parse(program)


if __name__ == "__main__":
    print(WARLOCK_GRAMMAR.parse(sys.stdin.read()))
