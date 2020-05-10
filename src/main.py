from tokenizer.tokenizer import Tokenizer
from parser.parser import Parser
import argparse

def test_file(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as testfile:
            file = testfile.read()
    except:
        raise Exception('File cannot be open!') # Don't! If you catch, likely to hide bugs.

    print("----------------------------TOKEN----------------------------")
    tokenizer = Tokenizer(file)
    tokenList, line = tokenizer.tokenize()
    for token in tokenList :
        print(token)

    print("-----------------------------AST-----------------------------")
    parser = Parser(tokenList, line)
    lines, errorList = parser.lineParser()
    for i in lines:
        print(i)

    print("----------------------------ERROR-----------------------------")
    for i in errorList.getErrorList():
        print(i)

    print("--------------------------NOTATION----------------------------")
    print("note : {}/5".format(errorList.calculNote()))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("-f", action='store', dest='file_name', help="file to test")
    args = parser.parse_args()
    test_file(args.file_name)
