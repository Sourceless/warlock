#!/usr/bin/env python3
import sys
from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor, rule


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

    statement = define / let / fn / fn_proto / trait / impl / macrodef / type / claim / macro

    define = "define" ws symbol ws expr
    let = "let" ws symbol ws expr
    fn = "fn" ws? "(" ws? symbol (ws? "," ws? symbol)* ")" ws? ":" ((ws expr) / (newline block))
    fn_proto = "fn" ws? "(" ws? symbol (ws? "," ws? symbol)* ")"
    trait = "trait" ws identifier ":" ((ws expr) / (newline block))
    impl = "impl" ws "for" ws identifier ":" ((ws expr) / (newline block))
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

    macro = &~r"." symbol? (ws arg)* (ws? args)? ":" ((newline block) / (ws expr))

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

class WarlockVisitor(NodeVisitor):
    def visit_newline(self, node, visited_children):
        return None

    def visit_identifier(self, node, visited_children):
        return node.text

    def visit_symbol(self, node, visited_children):
        _reserved, identifier = visited_children
        return identifier

    def visit_integer(self, node, visited_children):
        _, value = visited_children
        return value

    def visit_natural(self, node, visited_chilren):
        return int(node.text)

    def visit_statement(self, node, visited_children):
        return visited_children[0]

    def visit_lone_expr(self, node, visited_children):
        return visited_children[0]

    def visit_program(self, node, visited_children):
        _, lines, _ = visited_children
        return lines

    def visit_define(self, node, visited_children):
        _define, _, sym, _, expr = visited_children
        return ("define", sym[0], expr[0])

    def visit_lines(self, node, visited_children):
        line, other_lines, _ = visited_children
        line = line[0]

        if len(line) == 1:
            return other_lines
        if len(line) == 3:
            return line[0] + other_lines

    def visit_line(self, node, visited_children):
        return visited_children

    def visit_literal(self, node, visited_children):
        return visited_children[0]

    def visit_expr(self, node, visited_children):
        return visited_children

    def generic_visit(self, node, visited_children):
        rule_name = node.expr.as_rule()
        if node.expr_name in {"ws"}:
            return None
        if rule_name in {"newline?", "!reserved", "ws?", "comment?"}:
            return None
        if node.expr_name in {""}:
            return visited_children
        return (node.expr_name, visited_children or node)


def visit(parse_tree):
    return WarlockVisitor().visit(parse_tree)


if __name__ == "__main__":
    tree = parse(sys.stdin.read())
    ast = visit(tree)
    print(ast)
