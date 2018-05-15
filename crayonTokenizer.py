import sys
from crayonLexer import *

if __name__ == '__main__':
    filename = sys.argv[1]
    file = open("crayon.test")
    chars = file.read()
    file.close()
    
    # Assign characters to tokens
    tokens = crayonLex(chars)
    for token in tokens:
        print token