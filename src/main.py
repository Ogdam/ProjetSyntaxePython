from tokenizer.tokenizer import tokenizer
from parser.parser import ast

with open("../test.py", 'r', encoding='utf-8') as testfile:
    tokenList = testfile.read()

    print("----------------------------TOKEN----------------------------")
    tokenList = tokenizer(tokenList)
    for token in tokenList :
        print(token)


    print("-----------------------------AST-----------------------------")
    lines = ast(tokenList)
    print(ast)
