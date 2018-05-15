import lexer

def main():
    
    # Read crayon language source code test.lang and store it 
    
    content = ""
    with open('test.lang', 'r') as file:
        content = file.read()
        
    #print(content) 
    
    #
    # LEXER
    # 
    
    # Call lexer class and initialize with crayon language source code
    lex = lexer.Lexer(content)
    
    # Call Tokenize method
    tokens = lex.tokenize()
    
    
main()