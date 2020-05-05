from tokenizer.tokenizer import tokenizer
from parser2.parser import lineParser

with open("../test.py", 'r', encoding='utf-8') as testfile:
    tokenList = testfile.read()

    print("----------------------------TOKEN----------------------------")
    tokenList = tokenizer(tokenList)
    for token in tokenList :
        print(token)


    print("-----------------------------AST-----------------------------")
    lines = lineParser(tokenList)
    for i in lines:
        for j in i:
            print(j)
