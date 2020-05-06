import re
from .constants import (
 specialChars,
 typeWord,
 typeNumber,
 errorToken,
 endOfLine
)


class Tokenizer:
    token = []

    def __init__(self, file):
        self.file = file

    def tokenize(self):
        self.replaceSpecialChar()
        splitFile = re.split('\n', self.file)
        for splitLine in splitFile:
            if len(splitLine)<=0:
                continue
            flag=True
            split = re.split(' ', splitLine)
            for line in split :
                if re.search("\*.\*", line):
                    type = self.characterType(line)
                    if type != None:
                        self.token.append({'type': type })
                elif len(line)<=0 and flag :
                    self.token.append({'type': "space"})
                    continue
                elif len(line)<=0 and flag is False :
                    continue
                else:
                    try:
                        i = int(line)
                        self.token.append({'type': typeNumber, "value" : line})
                    except:
                        self.token.append({'type': typeWord, "value" : line})

                flag=False
            self.token.append({'type': endOfLine})

        if len(self.token)<=0:
            self.token.append({'type': errorToken })
        return self.token


    def characterType(self, char):
        for word in specialChars:
            if char in word['value']:
                return word["name"]

    def replaceSpecialChar(self):
        for word in specialChars:
            self.file = self.file.replace(word["regex"], word["value"])
