import crayonLexerFunction

# http://jayconrod.com/posts/37/a-simple-interpreter-from-scratch-in-python-part-1

# Language markers
KEYWORD = 'KEYWORD'
INT      = 'INT'
STRING   = 'STRING'
ID       = 'ID'

# Expression tokens including operators, keywords, strings and ints
expressionToks = [
    
    (r'[ \n\t]+',              None),
    (r'#[^\n]*',               None),
    (r'\:=',                   KEYWORD),
    
    (r'BLACK',                 STRING),
    
    (r'\(',                    KEYWORD),
    (r'\)',                    KEYWORD),
    (r';',                     KEYWORD),
    (r'\+',                    KEYWORD),
    (r'-',                     KEYWORD),
    (r'\*',                    KEYWORD),
    (r'/',                     KEYWORD),
    (r'<=',                    KEYWORD),
    (r'<',                     KEYWORD),
    (r'>=',                    KEYWORD),
    (r'>',                     KEYWORD),
    (r'=',                     KEYWORD),
    (r'!=',                    KEYWORD),
    
    # Testing keywords
    
    (r'and',                   KEYWORD),
    (r'or',                    KEYWORD),
    (r'not',                   KEYWORD),
    (r'if',                    KEYWORD),
    (r'then',                  KEYWORD),
    (r'else',                  KEYWORD),
    (r'while',                 KEYWORD),
    (r'do',                    KEYWORD),
    (r'end',                   KEYWORD),
    
    (r'RED',                   KEYWORD),
    (r'BLUE',                  KEYWORD),
    (r'PURPLE',                KEYWORD),
    (r'GREEN',                 KEYWORD),
    (r'YELLOW',                KEYWORD),

    
    (r'[0-9]+',                INT),
    (r'[A-Za-z][A-Za-z0-9_]*', ID),
    
]

def crayonLex(chars):
    return crayonLexerFunction.lex(chars, expressionToks)