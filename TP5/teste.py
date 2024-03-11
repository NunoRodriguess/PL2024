import ply.lex as lex
import sys

class MyClass(object):
# List of token names.   This is always required
    tokens = (
    'RWORDS',
    'WORDS',
    'STRINGS',
    'COMMA',
    'FLOAT',
    'INT',
    'OPERATION',
    'ASTERISCO',
    'LPAREN',
    'RPAREN',
    'SEMICOLON',
    )

    # Regular expression rules for simple tokens
    t_RWORDS  = r'[Ss][Ee][lL][eE][cC][tT] | [wW][hH][eE][rR][eE]|[fF][rR][oO][mM]'
    t_WORDS  = r'[a-zA-Z_]+'
    t_STRINGS  = r'\"[a-zA-Z_0-9.,:;!? ]+\" | \'[a-zA-Z_0-9.,:;!? ]+\''
    t_COMMA = r','
    t_OPERATION = r'[+\-><=/]+'
    t_ASTERISCO = r'\*'
    t_LPAREN  = r'\('
    t_RPAREN  = r'\)'
    t_SEMICOLON  = r';'

    # A regular expression rule with some action code
    def t_FLOAT(t):
        r'[+\-]?\d+\.\d+'
        t.value = float(t.value)    
        return t

    def t_INT(t):
        r'[+\-]?\d+'
        t.value = int(t.value)    
        return t


    # Define a rule so we can track line numbers
    def t_newline(t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # A string containing ignored characters (spaces and tabs)
    t_ignore  = ' \t'

    # Error handling rule
    def t_error(t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Build the lexer
    def __init__(self):
        self.lexer = lex.lex()

m = MyClass()
for line in sys.stdin:
    m.lexer.input(line)
    for tok in m.lexer:
        print(tok.type, tok.value, tok.lineno, tok.lexpos)