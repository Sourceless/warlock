from warlock.offside import analyze, count_indents


def test_count_indents():
    assert count_indents("") == 0
    assert count_indents(" ") == 0
    assert count_indents('print("Hello world!")') == 0

    assert count_indents("    ") == 1
    assert count_indents("     ") == 1
    assert count_indents('    print("Hello world!")') == 1

    assert count_indents("        ") == 2


def test_analyze():
    program = 'print("hello world")'
    assert analyze(program) == program

    program = 'def blah:\n    print("hello world")'
    assert analyze(program) == 'def blah:\nINDENT\nprint("hello world")\nDEDENT'

    program = 'def blah:\n    print("hello world")\n\nprint("something else")'
    assert analyze(program) == 'def blah:\nINDENT\nprint("hello world")\nDEDENT\nprint("something else")'

    program = 'def mutli_indent@\n    if True:\n        print("hello world")'
    assert analyze(program) == 'def mutli_indent@\nINDENT\nif True:\nINDENT\nprint("hello world")\nDEDENT\nDEDENT'
