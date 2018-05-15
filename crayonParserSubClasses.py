# ParseOutput on successful parse
class ParseOutput:
    
    # Output if succcessful will produce arguments for AST value and stack position
    def __init__(self, value, pos):
        
        # AST Value
        self.value = value
        
        # Index Position
        self.pos = pos
    
    def __repr__(self):
        return 'Output(%s, %d)' % (self.value, self.pos)

# Defining parser object to take a stream of input tokens
class Parser:
    
    # Call method takes full list of lexer tokens and position index
    def __call__(self, tokens, pos):
        return None # parser subclasses will return actuall call method

    # + Operator Definition 
    def __add__(self, other):
        return Link(self, other)

    # * Operator Definition
    def __mul__(self, other):
        return ExprMatch(self, other)

    # | OR operator definition
    def __or__(self, other):
        return Alternative(self, other)

    # ^ XOR operator definition
    def __xor__(self, function):
        return Process(self, function)
        
# Keyword parser to parse crayon language reserved words
# Each token is made up of pairs [0] is a value [1] is a marker
class Keyword(Parser):
    def __init__(self, value, marker):
        self.value = value
        self.marker = marker

    def __call__(self, tokens, pos):
        if pos < len(tokens) and \
           tokens[pos][0] == self.value and \
           tokens[pos][1] is self.marker:
            return ParseOutput(tokens[pos][0], pos + 1)
        else:
            return None

# Match any token with a specific marker ie: KEYWORD, INT, STRING 
class Marker(Parser):
    def __init__(self, marker):
        self.marker = marker

    def __call__(self, tokens, pos):
        if pos < len(tokens) and tokens[pos][1] is self.marker:
            return ParseOutput(tokens[pos][0], pos + 1)
        else:
            return None
            
# Link left and right parser input if both successfully produced a Parsed output, the new value will be a linked value
class Link(Parser):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __call__(self, tokens, pos):
        leftParseOutput = self.left(tokens, pos)
        if leftParseOutput:
            rightParseOutput = self.right(tokens, leftParseOutput.pos)
            if rightParseOutput:
                linkedValue = (leftParseOutput.value, rightParseOutput.value)
                return ParseOutput(linkedValue, rightParseOutput.pos)
        return None
        
# Alternative parser allows for seperated parsers
# By looking at left and right parsers and singling out specific tokens
class Alternative(Parser):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __call__(self, tokens, pos):
        leftParseOutput = self.left(tokens, pos)
        if leftParseOutput:
            return leftParseOutput
        else:
            rightParseOutput = self.right(tokens, pos)
            return rightParseOutput
            
# Statement parser is for optional statement clauses example else clause.
class Statement(Parser):
    def __init__(self, parser):
        self.parser = parser

    def __call__(self, tokens, pos):
        ParseOutput = self.parser(tokens, pos)
        if ParseOutput:
            return ParseOutput
        else:
            return ParseOutput(None, pos)

# List parser for generating or matching lists, repeats until fails. 
class List(Parser):
    def __init__(self, parser):
        self.parser = parser

    def __call__(self, tokens, pos):
        ParseOutputs = []
        ParseOutput = self.parser(tokens, pos)
        while ParseOutput:
            ParseOutputs.append(ParseOutput.value)
            pos = ParseOutput.pos
            ParseOutput = self.parser(tokens, pos)
        return ParseOutput(ParseOutputs, pos)

# Allows manipulation of output values, used to build abstract syntax tree
class Process(Parser):
    def __init__(self, parser, function):
        self.parser = parser
        self.function = function

    def __call__(self, tokens, pos):
        ParseOutput = self.parser(tokens, pos)
        if ParseOutput:
            ParseOutput.value = self.function(ParseOutput.value)
            return ParseOutput

# Efficiency parser only computes values to be used depending on relevant markers
class Efficiency(Parser):
    def __init__(self, parserFunc):
        self.parser = None
        self.parserFunc = parserFunc

    def __call__(self, tokens, pos):
        if not self.parser:
            self.parser = self.parserFunc()
        return self.parser(tokens, pos)

# Garbage bypass parser prevents parsing garbage by checking matches against length
class GarbageBypass(Parser):
    def __init__(self, parser):
        self.parser = parser

    def __call__(self, tokens, pos):
        ParseOutput = self.parser(tokens, pos)
        if ParseOutput and ParseOutput.pos == len(tokens):
            return ParseOutput
        else:
            return None

# Expression Match 
    # Match epression containing a list of elements or multiple statements seperated by something semi-colon
    # Takes a parser and a separator to match element of list and semicolon seperator
    # On success combines seperator and parser into next process
    
class ExprMatch(Parser):
    def __init__(self, parser, separator):
        self.parser = parser
        self.separator = separator

    def __call__(self, tokens, pos):
        ParseOutput = self.parser(tokens, pos)

        # Combine matched expressions
        def processNext(parsed):
            (sepfunc, right) = parsed
            return sepfunc(ParseOutput.value, right)
        nextParser = self.separator + self.parser ^ processNext

        nextParseOutput = ParseOutput
        while nextParseOutput:
            nextParseOutput = nextParser(tokens, ParseOutput.pos)
            if nextParseOutput:
                ParseOutput = nextParseOutput
        return ParseOutput            






