import argparse
import ox
from collections import namedtuple

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("filename", help="Lispfuck filename")

args = arg_parser.parse_args()
INPUT_FILENAME = args.filename


def tokenize(code):
    lexer = ox.make_lexer([
        ('PAREN_O', r'\('),
        ('PAREN_C', r'\)'),
        ('DO', r'do'),
        ('DO_AFTER', r'do-after'),
        ('DO_BEFORE', r'do-before'),
        ('READ', r'read'),
        ('INC', r'inc'),
        ('DEC', r'dec'),
        ('ADD', r'add'),
        ('SUB', r'sub'),
        ('RIGHT', r'right'),
        ('LEFT', r'left'),
        ('PRINT', r'print'),
        ('LOOP', r'loop'),
        # ('FUNC', r'def \s([a-zA-Z]*)'),
        # ('PARAM', r'[a-zA-Z]'),
        ('COMMENT', r';.*'),
        ('NEWLINE', r'\n'),
        ('SPACE', r'\s+'),
        ('NUMBER', r'[0-9]+')
    ])
    return lexer(code)


token_list = ['PAREN_O', 'PAREN_C', 'DO', 'DO_AFTER',
              'DO_BEFORE', 'READ', 'INC', 'DEC', 'ADD', 'SUB',
              'RIGHT', 'LEFT', 'PRINT', 'LOOP', 'FUNC', 'ID', 'NUMBER'
             ]


def parse(tokens):
    parser = ox.make_parser([
        ('func : PAREN_O name args PAREN_C', lambda x, y, z, w: (y, z)),
        ('name : DO', lambda x: x),
        ('name : ADD', lambda x: x),
        ('name : SUB', lambda x: x),
        ('name : LOOP', lambda x: x),
        ('args : args arg', lambda x, y: x + [y]),
        ('args : arg', lambda x: [x]),
        ('arg : func', lambda x: x),
        ('arg : procedure', lambda x: x),
        ('arg : NUMBER', lambda x: x),
        ('procedure : PRINT', lambda x: x),
        ('procedure : INC', lambda x: x),
        ('procedure : DEC', lambda x: x),
        ('procedure : READ', lambda x: x),
        ('procedure : LEFT', lambda x: x),
        ('procedure : RIGHT', lambda x: x),

    ], token_list)

    return parser(tokens)


def arguments(args1, args2):
    if type(args2) is list:
        return args1 + args2
    else:
        args1.append(args2)
        return args1


def do_before(p_o1, d_b, args1, p_o2, args2, p_c1, p_c2):
    result = []

    for i in args2:
        for j in args1:
            result.append(j)

        result.append(i)

    return ('Do', result)


def do_after(p_o1, d_a, args1, p_o2, args2, p_c1, p_c2):
    result = []

    for i in args2:
        result.append(i)
        for j in args1:
            result.append(j)

    return ('Do', result)


def validate_arg(arg):
    result = []
    if arg is not None:
        result.append(arg)

    return result



if __name__ == '__main__':
    arquivolf = open(INPUT_FILENAME, 'r')
    code = arquivolf.read()
    tokens = tokenize(code)
    clean_tokens = []

    for token in tokens:
        if token.type != 'SPACE' and token.type != 'COMMENT':
            clean_tokens.append(token)

    print(clean_tokens)
    print(parse(clean_tokens))
