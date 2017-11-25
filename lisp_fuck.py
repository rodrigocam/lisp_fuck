import ox
import argparse
from collections import namedtuple

parser = argparse.ArgumentParser()
parser.add_argument("filename", help="Lispfuck filename")

args = parser.parse_args()
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
        ('RIGHT', r'right'),
        ('LEFT', r'left'),
        ('PRINT', r'print'),
        ('LOOP', r'loop'),
        ('FUNC', r'def \s([a-zA-Z]*)'),
        ('PARAM', r'[a-zA-Z]{1}'),
        ('COMMENT', r';.*'),
        ('NEWLINE', r'\n'),
        ('SPACE', r'\s+')
    ])
    return lexer(code)


token_list = ['PAREN_O', 'PAREN_C', 'DO', 'DO_AFTER',
                 'DO_BEFORE', 'READ', 'INC', 'DEC', 'ADD',
                 'RIGHT', 'LEFT', 'PRINT', 'LOOP', 'FUNC', 'ID'
                ]

def parse(tokens):
    parser = ox.make_parser([
        ('def : do FUNC PAREN_O args PAREN_C PAREN_O args PAREN_C', test),
        ('do : do arg', lambda d, a: d),
        ('do : PAREN_O DO args PAREN_C', lambda p_o, do, args, p_c: ('DO', args)),
        ('do : PAREN_O DO_AFTER args PAREN_O args PAREN_C PAREN_C', do_after),
        ('do : PAREN_O DO_BEFORE args PAREN_O args PAREN_C PAREN_C', do_before),
        ('args : loop', lambda x:x),
        ('loop : PAREN_O LOOP args PAREN_C', lambda p_o, loop, args, p_c: ('Loop', args)),
        ('args : args args', arguments),
        ('args : args arg', arguments),
        ('args : arg', validate_arg),
        ('arg : READ', lambda x:x),
        ('arg : INC', lambda x:x),
        ('arg : DEC', lambda x:x),
        ('arg : ADD', lambda x:x),
        ('arg : RIGHT', lambda x:x),
        ('arg : LEFT', lambda x:x),
        ('arg : PRINT', lambda x:x),

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