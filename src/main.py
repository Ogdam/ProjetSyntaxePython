from tokenizer.tokenizer import Tokenizer
from parser2.parser import lineParser

with open("../test.py", 'r', encoding='utf-8') as testfile:
    file = testfile.read()

    print("----------------------------TOKEN----------------------------")
    tokenizer = Tokenizer(file)
    tokenList = tokenizer.tokenize()
    for token in tokenList :
        print(token)


    # print("-----------------------------AST-----------------------------")
    # lines = lineParser(tokenList)
    # for i in lines:
    #     for j in i:
    #         print(j)
