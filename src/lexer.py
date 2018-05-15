import re

class Lexer(object):
    
    # add user select file
    # https://www.youtube.com/watch?v=4qWvOLl5dZU
    
    # Parse statements
    # http://jayconrod.com/posts/39/a-simple-interpreter-from-scratch-in-python-part-3
    
    # https://www.youtube.com/watch?v=4qWvOLl5dZU
    # initiate class
    def __init__(self, source_code):
        self.source_code = source_code
        
    # Tokenize method to turn source code into tokens
    def tokenize(self):
        
        #print('test')
        
        # Store all tokens created by lexer
        tokens = []
        
        # Source code holds a list of all words in crayon test.lang
        source_code = self.source_code.split()
        
        # Source index holds word index when looping through source code
        source_index = 0
        
        # Loop through source code and print every word item
        while source_index < len(source_code):
            
            # Store current word in loop
            word = source_code[source_index]
            
            ###### VAR CHANGE TO CRAYON # Recognize var and create VAR_DECLARATION for it
            if word == "var": tokens.append(["VAR_DECLARATION", word])
            
            # Recognize word before creating IDENTIFIER token for it 
            elif re.match('[a-z]', word) or re.match('A-Z', word):
                tokens.append(['IDENTIFIER', word])
            
            ##### INT CHANGE TO CRAYON Recognize integer token and append it
            ## 
            elif re.match('[0-9]', word):
                tokens.append(['INTEGER', word])
             
            # Recognise operators then create OPERATOR for it
            elif word in "=/*=-+":
                tokens.append(['OPERATOR', word])
                
            # Increase word index after check
            source_index += 1
        
        print(tokens)
        
        # Created tokens
        return tokens