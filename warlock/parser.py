#!/usr/bin/env python3
import sys
from parsimonious.grammar import Grammar


WARLOCK_GRAMMAR = Grammar(
    r"""
    program = newline? lines newline?
    lines = line (newline line)* ws?
    line = comment / (expr ws? comment?)
    expr = infix_expr / lone_expr
    lone_expr = statement / call / literal / symbol
    infix_expr = lone_expr ws infix_identifier_inner ws expr
    comment = "#" ~r".*"

    reserved = "INDENT" / "DEDENT" / "define" / "let" / "fn" / "macro" / "type" / "->"

    newline = ~r"\n+"
    ws = ~r" +"
    block = "INDENT" newline lines newline "DEDENT"
    args = "(" ws? (arg ("," ws? arg)*)? ws? ")"
    arg = call / type_exprs / expr

    statement = define / let / fn / macrodef / type / claim / macro

    define = "define" ws symbol ws expr
    let = "let" ws symbol ws expr
    fn = "fn" ws? "(" ws? identifier (ws? "," ws? identifier)* ")" ws? ":" ((ws expr) / (newline block))
    macrodef = "macro" ws? "(" ws? identifier (ws? "," ws? identifier)* ")" ws? ":" ((ws expr) / (newline block))
    type = "type" ws identifier ws? ":" ws? typedef
    call = symbol ws? args

    typedef = type_exprs (ws? "|" ws? type_exprs)
    type_exprs = type_expr (ws type_expr)*
    type_expr = unit / symbol_group / symbol
    unit = "()"
    symbol_group = "(" ws? symbol (ws symbol)* ws? ")"

    claim = symbol ws? ":" ws? claim_exprs
    claim_exprs = claim_expr (ws "->" ws claim_expr)*
    claim_expr = claim_group / type_exprs
    claim_group = "(" ws? claim_exprs ws? ")"

    macro = block_macro_bare / block_macro_call / block_macro_args
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
    print(parse(sys.stdin.read()))
