# DESCRIPTION
# TODO

class Equality:
    def __eq__(self, other):
        return isinstance(other, self.__class__) and \
               self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

# Statements used for all statements
class Statement(Equality):
    pass

# Arithmatic expressions used for number computations
class Expressions(Equality):
    pass

# Boolean expressions used for conditionals
class BoolExpressions(Equality):
    pass

class AssignStatement(Statement):
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression

    def __repr__(self):
        return 'AssignStatement(%s, %s)' % (self.name, self.expression)

    def eval(self, env):
        value = self.expression.eval(env)
        env[self.name] = value
        
class AssignString(Statement):
    def __init__(self, name, strin):
        self.name = name
        self.strin = strin

    def __repr__(self):
        return 'AssignString(%s, %s)' % (self.name, self.strin)
        
    def eval(self, env):
        value = self.strin
        env[self.name] = value

class MultipleStatement(Statement):
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __repr__(self):
        return 'MultipleStatement(%s, %s)' % (self.first, self.second)

    def eval(self, env):
        self.first.eval(env)
        self.second.eval(env)

class IfStatement(Statement):
    def __init__(self, condition, trueStatement, falseStatement):
        self.condition = condition
        self.trueStatement = trueStatement
        self.falseStatement = falseStatement

    def __repr__(self):
        return 'IfStatement(%s, %s, %s)' % (self.condition, self.trueStatement, self.falseStatement)

    def eval(self, env):
        conditionValue = self.condition.eval(env)
        if conditionValue:
            self.trueStatement.eval(env)
        else:
            if self.falseStatement:
                self.falseStatement.eval(env)

class WhileStatement(Statement):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return 'WhileStatement(%s, %s)' % (self.condition, self.body)

    def eval(self, env):
        conditionValue = self.condition.eval(env)
        while conditionValue:
            self.body.eval(env)
            conditionValue = self.condition.eval(env)
 
class ForLoop(Statement):
    def __init__(self, name, expression, condition, body):
        self.name = name
        self.expression = expression
        self.condition = condition
        self.body = body

    def __repr__(self):
        return 'ForLoop(%s, %s, %s, %s)' % (self.name, self.expression, self.condition, self.body)

    def eval(self, env):
        value = self.expression.eval(env)
        env[self.name] = value
        conditionValue = self.condition.eval(env)
        while conditionValue:
            self.body.eval(env)
            conditionValue = self.condition.eval(env)
            

class IntAexp(Expressions):
    def __init__(self, i):
        self.i = i

    def __repr__(self):
        return 'IntAexp(%d)' % self.i

    def eval(self, env):
        return self.i
        
class FloatAexp(Expressions):
    def __init__(self, f):
        self.f = f

    def __repr__(self):
        return 'FloatAexp(%d)' % self.f

    def eval(self, env):
        return self.f

class VarAexp(Expressions):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'VarAexp(%s)' % self.name

    def eval(self, env):
        if self.name in env:
            return env[self.name]
        else:
            return 0
            
class StringExp(Expressions):
    def __init__(self, strin):
        self.strin = strin

    def __repr__(self):
        return 'StringExp(%s)' % self.strin

    def eval(self, env):
        if self.strin in env:
            return env[self.strin]
        else:
            return 0
            
class PrintExp(Expressions):
    def __init__(self, prnt):
        self.prnt = prnt

    def __repr__(self):
        return 'PrintExp(%s)' % self.prnt

    def eval(self, env):
        if self.prnt in env:
            return env[self.prnt]
        else:
            return 0

class BinopAexp(Expressions):
    def __init__(self, operation, left, right):
        self.operation = operation
        self.left = left
        self.right = right

    def __repr__(self):
        return 'BinopAexp(%s, %s, %s)' % (self.operation, self.left, self.right)

    def eval(self, env):
        leftValue = self.left.eval(env)
        rightValue = self.right.eval(env)
        if self.operation == '+':
            value = leftValue + rightValue
        elif self.operation == '-':
            value = leftValue - rightValue
        elif self.operation == '*':
            value = leftValue * rightValue
        elif self.operation == '/':
            value = leftValue / rightValue
        else:
            raise RuntimeError('unknown operator: ' + self.operation)
        return value

class RelopBexp(BoolExpressions):
    def __init__(self, operation, left, right):
        self.operation = operation
        self.left = left
        self.right = right

    def __repr__(self):
        return 'RelopBexp(%s, %s, %s)' % (self.operation, self.left, self.right)

    def eval(self, env):
        leftValue = self.left.eval(env)
        rightValue = self.right.eval(env)
        if self.operation == '<':
            value = leftValue < rightValue
        elif self.operation == '<=':
            value = leftValue <= rightValue
        elif self.operation == '>':
            value = leftValue > rightValue
        elif self.operation == '>=':
            value = leftValue >= rightValue
        elif self.operation == '=':
            value = leftValue == rightValue
        elif self.operation == '!=':
            value = leftValue != rightValue
        else:
            raise RuntimeError('unknown operator: ' + self.operation)
        return value

class AndBoolExpression(BoolExpressions):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return 'AndBoolExpression(%s, %s)' % (self.left, self.right)

    def eval(self, env):
        leftValue = self.left.eval(env)
        rightValue = self.right.eval(env)
        return leftValue and rightValue

class OrBoolExpression(BoolExpressions):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return 'OrBoolExpression(%s, %s)' % (self.left, self.right)

    def eval(self, env):
        leftValue = self.left.eval(env)
        rightValue = self.right.eval(env)
        return leftValue or rightValue

'''        
class PrintExpression(PrintExpressions):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return 'PrintExpression(%s, %s)' % (self.left, self.right)

    def eval(self, env):
        leftValue = self.left.eval(env)
        rightValue = self.right.eval(env)
        return leftValue or rightValue
'''

class NotBoolExpression(BoolExpressions):
    def __init__(self, exp):
        self.exp = exp

    def __repr__(self):
        return 'NotBoolExpression(%s)' % self.exp

    def eval(self, env):
        value = self.exp.eval(env)
        return not value
