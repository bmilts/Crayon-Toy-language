from crayonKeywords import *
from crayonParserSubClasses import *
from crayonSyntaxTree import *

# Basic parsers

# Keyword parser 
def keyword(kw):
    return Keyword(kw, KEYWORD)
    
# Convert values returned by num, id into expressions          
def expressionValue():
    return (num ^ (lambda i: IntAexp(i))) | \
           (id  ^ (lambda v: VarAexp(v))) | \
           (str  ^ (lambda s: StringExp(s))) | \
           (numFloat  ^ (lambda f: FloatExp(f))) | \
           (printVal  ^ (lambda prnt: PrintExp(prnt)))

# Convert number token into an integer value
num = Marker(INT) ^ (lambda i: int(i))
numFloat = Marker(FLOAT) ^ (lambda f: float(f))

# Convert ID token into python id
id = Marker(ID)
str = Marker(ID)
printVal = Marker(BROWN)

# Top level parser
def crayonParse(tokens):
    ast = parser()(tokens, 0)
    return ast

def parser():
    return HighLevelParse(statementList())    

# Multiple Statement seperator
def statementList():
    separator = keyword('BLUE') ^ (lambda x: lambda l, r: MultipleStatement(l, r))
    return ExprMatch(statement(), separator)

# 
def statement():
    return statementAssign() | \
           statementIf()     | \
           statementWhile()  | \
           stringAssign()    | \
           statementFor()
           
# NOTE ****** Assigne variable delimit
def statementAssign():
    def process(parsed):
        ((name, _), exp) = parsed
        return AssignStatement(name, exp)
    return id + keyword('RED') + expression() ^ process

# Assigns Strings to   
def stringAssign():
    def process(parsed):
        ((name, _), strin) = parsed
        return AssignString(name, strin)
    return id + keyword('BLACK') + str ^ process
    
# If statement logic parser
def statementIf():
    def process(parsed):
        (((((_, condition), _), statementTrue), parsedFalse), _) = parsed
        if parsedFalse:
            (_, statementFalse) = parsedFalse
        else:
            statementFalse = None
        return IfStatement(condition, statementTrue, statementFalse)
            # if, then, else, end
    return keyword('PURPLE') + boolExpressions() + \
           keyword('GREEN') + Efficiency(statementList) + \
           Optional(keyword('YELLOW') + Efficiency(statementList)) + \
           keyword('TAN') ^ process

# While statement parse logic
def statementWhile():
    def process(parsed):
        ((((_, condition), _), body), _) = parsed
        return WhileStatement(condition, body)
        # While, do, end
    return keyword('VIOLET') + boolExpressions() + \
           keyword('ORANGE') + Efficiency(statementList) + \
           keyword('TAN') ^ process

# ATTEMPTED FOR LOOP
def statementFor():
    def process(parsed):
        (((((((name, _), exp), _), condition), _), body), _) = parsed
        return ForLoop(name, exp, condition, body)
        # for, name/expression, do, end
    return id + keyword('RED') + expression() + \
           keyword('PEAR') + boolExpressions() + \
           keyword('ORANGE') + Efficiency(statementList) + \
           keyword('TAN') ^ process

# Boolean expressions
def boolExpressions():
    return precedence(boolExpressionTerm(),
                      boolExpressionPrecedence,
                      parseLogic)

# Boolean expression terms 
def boolExpressionTerm():
    return boolExpressionNot()   | \
           boolExpressionOperate() | \
           boolExpressionGroup()

# Not operator expression parser
def boolExpressionNot():
    return keyword('WHITE') + Efficiency(boolExpressionTerm) ^ (lambda parsed: NotBoolExpression(parsed[1]))

# Boolean expression operation parser
def boolExpressionOperate():
    operator = ['<', '<=', '>', '>=', '=', '!=']
    return expression() + operatorList(operator) + expression() ^ parseOperator

# Boolean expression group
def boolExpressionGroup():
    return keyword('(') + Efficiency(boolExpressions) + keyword(')') ^ parseGroup

# In expressions
def expression():
    return precedence(expressionTerm(),
                      expressionPrecedence,
                      parseBinaryOperation)

# Combine expressions and expression groupes 
def expressionTerm():
    return expressionValue() | expressionGroup()

def expressionGroup():
    return keyword('(') + Efficiency(expression) + keyword(')') ^ parseGroup

# Precedence parser subclass for binary operator expressions
def precedence(valueParser, precedenceLevels, combine):
    def parseOperations(precedenceLevel):
        return operatorList(precedenceLevel) ^ combine
    parser = valueParser * parseOperations(precedenceLevels[0])
    for precedenceLevel in precedenceLevels[1:]:
        parser = parser * parseOperations(precedenceLevel)
    return parser

# Functions to parse binary and relational operators
def parseBinaryOperation(operation):
    return lambda l, r: BinopAexp(operation, l, r)
    
# 
def parseOperator(parsed):
    ((left, operation), right) = parsed
    return RelopBexp(operation, left, right)

# and, or
def parseLogic(operation):
    if operation == 'APRICOT':
        return lambda l, r: AndBoolExpression(l, r)
    elif operation == 'FERN':
        return lambda l, r: OrBoolExpression(l, r)
    else:
        raise RuntimeError('Unaccepted crayon logic operator: ' + operation)

# Parse a group of terms by removing parenthesies
def parseGroup(parsed):
    ((_, p), _) = parsed
    return p

def operatorList(operationList):
    operatorParser = [keyword(operation) for operation in operationList]
    parser = reduce(lambda l, r: l | r, operatorParser)
    return parser
    
# Operator keywords and precedence levels
expressionPrecedence = [
    ['*', '/'],
    ['+', '-'],
]

# Boolean operations precedence
boolExpressionPrecedence = [
    ['APRICOT'],
    ['FERN'],
]
