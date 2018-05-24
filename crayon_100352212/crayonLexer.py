import sys
import re

# Takes chars and expression functions and compares them to python regular expressions
def lex(chars, expressionToks):
    
    pos = 0
    tokens = []

    while pos < len(chars):
        match = None
        for expressionTok in expressionToks:
            pattern, marker = expressionTok
            regex = re.compile(pattern)
            match = regex.match(chars, pos)
            if match:
                text = match.group(0)
                if marker:
                    token = (text, marker)
                    tokens.append(token)
                break
            
        # Error checking 
        if not match:
            sys.stderr.write('Unaccepted crayon char: %s\\n' % chars[pos])
            sys.exit(1)
        else:
            pos = match.end(0)
    return tokens