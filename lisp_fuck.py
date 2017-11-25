import argparse
import ox
import pprint
from ox import Token as ox_token
import re
from collections import namedtuple

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("filename", help="Lispfuck filename")

args = arg_parser.parse_args()
INPUT_FILENAME = args.filename

regex_map = [
    ('PAREN_O', r'\('),
    ('PAREN_C', r'\)'),
    ('DO', r'do'),
    ('DO_AFTER', r'do-after'),
    ('DO_BEFORE', r'do-before'),
    ('READ', r'read'),
    ('INC', r'inc'),
    ('DEC', r'dec'),
    ('DEF', r'def'),
    ('ADD', r'add'),
    ('SUB', r'sub'),
    ('RIGHT', r'right'),
    ('LEFT', r'left'),
    ('PRINT', r'print'),
    ('LOOP', r'loop'),
    ('COMMENT', r';.*'),
    ('NEWLINE', r'\n'),
    ('SPACE', r'\s'),
    ('NUMBER', r'[0-9]+')
]

valid_tokens = [x for x, y in regex_map]
valid_tokens.append('FUNC_NAME')

template = r'(?P<{name}>{regex})'

# This is used to create a big regex with all
# regex in regex_map to avoid compile one regex
# at a time
REGEX_ALL = '|'.join(
    template.format(name=name, regex=regex)
    for (name, regex) in regex_map
)

re_all = re.compile(REGEX_ALL)


def tokenize(source):
    """
    Return each token  of a given string based on lexer rules
    """
    token_list = []
    lineno = 1
    last = 0
    for m in re_all.finditer(source):
        type_ = m.lastgroup
        i, j = m.span()
        if i > last:
            # it means that there is text between last match and this one
            token_list.append(Token('FUNC_NAME', source[last:i], lineno))
        last = j
        data = m.string[i:j]
        token_list.append(Token(type_, data, lineno))

    if last != len(source):
        token_list.append(Token('FUNC_NAME', source[last:len(source)], lineno))

    return token_list


class Token(ox_token):
    """
    The Token definition used by jarbas_dsl lexer
    is the same used by the ox-parse lib
    """
    def __gt__(self, other):
        if isinstance(other, Token):
            return self.value > other.value
        elif isinstance(other, str):
            return self.value > other
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Token):
            return self.value < other.value
        elif isinstance(other, str):
            return self.value < other
        return NotImplemented


no_func = lambda x: x


def func_def_args(p_o, d, func_name, params, p_o2, func_code, p_c2 , p_c):
    return ('func_def', (func_name, (params, func_code)))


def func_def_func(p_o, d, func_name, params, func_code, p_c):
    return ('func_def', (func_name, (params, func_code)))


def parse(tokens):
    parser = ox.make_parser([
        ('func : PAREN_O DO_AFTER args PAREN_O args PAREN_C PAREN_C', do_after),
        ('func : PAREN_O DO_BEFORE args PAREN_O args PAREN_C PAREN_C', do_before),
        ('func : PAREN_O FUNC_NAME args PAREN_C', lambda x, y, z, w: (y, z)),
        ('func : PAREN_O name args PAREN_C', lambda x, y, z, w: (y, z)),
        ('func_def : PAREN_O DEF FUNC_NAME params func PAREN_C', func_def_func),
        ('func_def : PAREN_O DEF FUNC_NAME params PAREN_O args PAREN_C PAREN_C', func_def_args),
        ('params : PAREN_O PAREN_C', lambda x, y: None),
        ('params : PAREN_O param PAREN_C', lambda x, y, z: y),
        ('param : param FUNC_NAME', lambda x, y: x + [y]),
        ('param : FUNC_NAME', lambda x: [x]),
        ('name : DO', no_func),
        ('name : ADD', no_func),
        ('name : SUB', no_func),
        ('name : LOOP', no_func),
        ('args : args arg', lambda x, y: x + [y]),
        ('args : arg', lambda x: [x]),
        ('arg : func', no_func),
        ('arg : func_def', no_func),
        ('arg : procedure', no_func),
        ('arg : NUMBER', no_func),
        ('procedure : FUNC_NAME', no_func),
        ('procedure : PRINT', no_func),
        ('procedure : INC', no_func),
        ('procedure : DEC', no_func),
        ('procedure : READ', no_func),
        ('procedure : LEFT', no_func),
        ('procedure : RIGHT', no_func),

    ], valid_tokens)

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
        if token.type != 'SPACE' and token.type != 'NEWLINE' and token.type != 'COMMENT':
            clean_tokens.append(token)

    print(pprint.pformat(clean_tokens))
    print(pprint.pformat(parse(clean_tokens)))
