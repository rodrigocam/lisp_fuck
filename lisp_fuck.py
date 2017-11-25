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

no_func = lambda x: x

def parse(tokens):
    parser = ox.make_parser([
        ('func : PAREN_O DO_AFTER args PAREN_O args PAREN_C PAREN_C', do_after),
        ('func : PAREN_O DO_BEFORE args PAREN_O args PAREN_C PAREN_C', do_before),
        ('func : PAREN_O name args PAREN_C', lambda x, y, z, w: (y, z)),
        ('name : DO', no_func),
        ('name : ADD', no_func),
        ('name : SUB', no_func),
        ('name : LOOP', no_func),
        ('args : args arg', lambda x, y: x + [y]),
        ('args : arg', lambda x: [x]),
        ('arg : func', no_func),
        ('arg : procedure', no_func),
        ('arg : NUMBER', no_func),
        ('procedure : PRINT', no_func),
        ('procedure : INC', no_func),
        ('procedure : DEC', no_func),
        ('procedure : READ', no_func),
        ('procedure : LEFT', no_func),
        ('procedure : RIGHT', no_func),

    ], token_list)

    return parser(tokens)



def do_before(p_o1, d_b, args1, p_o2, args2, p_c1, p_c2):
    result = []

    for i in args2:
        partial_result = args1[:]
        partial_result.append(i)

        element = ('do', partial_result)
        result.append(element)

    return ('do', result)


def do_after(p_o1, d_a, args1, p_o2, args2, p_c1, p_c2):
    result = []

    for i in args2:
        partial_result = []
        partial_result.append(i)
        partial_result += args1

        element = ('do', partial_result)
        result.append(element)

    return ('do', result)


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
