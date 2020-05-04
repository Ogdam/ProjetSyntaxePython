from .constants import specialChars
import re

def replaceSpecialChar(file):
    for word in specialChars:
        file = file.replace(word["value"], " *{}* ".format(word["value"]))
    return file


def tokenizer(file):
    file = replaceSpecialChar(file)
    token = re.split('\f\v\t', file)
    print(len(token))
