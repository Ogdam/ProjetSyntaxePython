import re
from .constants import (
 specialChars,
 typeWord,
 typeNumber,
 errorToken,
 endOfLine
)

def characterType(char):
    for word in specialChars:
        if char in word['value']:
            return word["name"]

def replaceSpecialChar(file):
    for word in specialChars:
        file = file.replace(word["regex"], word["value"])
    return file


def tokenizer(file):
    file = replaceSpecialChar(file)
    splitFile = re.split('\n', file)
    token = []
    for splitLine in splitFile:
        if len(splitLine)<=0:
            continue
        flag=True
        split = re.split(' ', splitLine)
        for line in split :
            if re.search("\*.\*", line):
                type = characterType(line)
                if type != None:
                    token.append({'type': type })
            elif len(line)<=0 and flag :
                token.append({'type': "space"})
                continue
            elif len(line)<=0 and flag is False :
                continue
            else:
                try:
                    i = int(line)
                    token.append({'type': typeNumber, "value" : line})
                except:
                    token.append({'type': typeWord, "value" : line})

            flag=False
        token.append({'type': endOfLine})

    if len(token)<=0:
        token.append({'type': errorToken })
    return token
