#!/usr/bin/env python3
"""
Offside rule pre-lexer
"""
import sys


OFFSIDE = "    "  # Four spaces only


def analyze(program):
    indent_level = 0
    reconstructed_lines = []

    for line in program.splitlines():
        indents = count_indents(line)

        if indents > indent_level:
            reconstructed_lines += ["INDENT"] * (indents - indent_level)
            indent_level = indents
        elif indents < indent_level:
            reconstructed_lines += ["DEDENT"] * (indent_level - indents)
            indent_level = indents

        if line != "":
            reconstructed_lines.append(line.lstrip(" "))

    if indent_level > 0:
        reconstructed_lines += ["DEDENT"] * indent_level

    return "\n".join(reconstructed_lines)


def count_indents(line):
    indents = 0

    unconsumed = line[:]
    while True:
        if unconsumed.startswith(OFFSIDE):
            indents += 1
            unconsumed = unconsumed[len(OFFSIDE):]
        else:
            break

    return indents


if __name__ == "__main__":
    print(analyze(sys.stdin.read()))
