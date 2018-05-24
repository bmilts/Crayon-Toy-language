#!/usr/bin/env python

import sys
from crayonParser import *
from crayonKeywords import *

def getFile(choices):
  choice = ""
  while choice not in choices:
      choice = raw_input("Please type the full name of the file to test: [%s]:" % ", ".join(choices))
  return choice

def usage():
    sys.stderr.write('To run Crayon please enter a test file example: file.crayon \n')
    sys.exit(1)

if __name__ == '__main__':
    #if len(sys.argv) != 2:
        #usage()
    
    #userinput = raw_input('Please enter name of test file: ')

    choice = getFile(["examples/test1.crayon", "examples/test2.crayon", "examples/test3.crayon", "examples/test4.crayon", "examples/test5.crayon"])

    text = open(choice).read()

    tokens = crayonLex(text)
    parse_result = crayonParse(tokens)
    if not parse_result:
        sys.stderr.write('Parse error!\n')
        sys.exit(1)
    ast = parse_result.value
    env = {}
    ast.eval(env)

    sys.stdout.write('\nAccepted tokens:\n\n')
    for token in tokens:
        print token

    sys.stdout.write('\n%s Language Input:\n' % choice)
    print text

    sys.stdout.write('\nCrayon Language file: %s results:\n\n' % choice)
    for name in env:
        sys.stdout.write('%s: %s\n' % (name, env[name]))
      
    finish = raw_input('\nWould you like to run another crayon test file?: [y/n] ')
    if not finish or finish[0].lower() !='y':
        print('\nThank you for testing crayon.\n')
        exit(1) 
    else:
        choice = getFile(["examples/test1.crayon", "examples/test2.crayon", "examples/test3.crayon", "examples/test4.crayon", "examples/test5.crayon"])
      
    