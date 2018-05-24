import crayonLexer

# Language markers
KEYWORD = 'KEYWORD'
INT      = 'INT'
ID       = 'ID'
FLOAT   = 'FLOAT' 
BROWN   = 'BROWN'

# Expression tokens including operators, keywords, strings and ints
expressionToks = [
    
    (r'[ \n\t]+',              None),
    (r'#[^\n]*',               None),
    
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
    (r'\%',                    KEYWORD),
    
    # Testing keywords

    (r'TEST',                  KEYWORD), # TEST
    (r'RED',                   KEYWORD), # Var keyword
    (r'BLUE',                  KEYWORD), # Multiple statement delimeter
    (r'PURPLE',                KEYWORD), # if 
    (r'GREEN',                 KEYWORD), # then
    (r'YELLOW',                KEYWORD), # Else
    (r'VIOLET',                KEYWORD), # While
    (r'ORANGE',                KEYWORD), # Do
    (r'TAN',                   KEYWORD), # End
    (r'APRICOT',               KEYWORD), # and
    (r'FERN',                  KEYWORD), # or
    (r'WHITE',                 KEYWORD), # not
    (r'PEAR',                  KEYWORD), # for
    (r'BLACK',                 KEYWORD), # String
    
    (r'[0-9]+',                INT),
    (r'[A-Za-z][A-Za-z0-9_]*', ID),
    (r'\d+[eE][-+]?\d+|(\.\d+|\d+\.\d+)([eE][-+]?\d+)?', FLOAT),
    
]

def crayonLex(chars):
    return crayonLexer.lex(chars, expressionToks)