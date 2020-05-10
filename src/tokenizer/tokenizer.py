import re
from .constants import Constants


class Tokenizer:
    token = []
    line = 0

    def __init__(self, file):
        self.file = file

    def tokenize(self):
        self.replaceSpecialChar()
        splitFile = re.split('\n', self.file)
        self.line = len(splitFile)
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
                        self.token.append({'type': Constants.typeNumber.value, "value" : line})
                    except:
                        self.token.append({'type': Constants.typeWord.value, "value" : line})

                flag=False
            self.token.append({'type': Constants.endOfLine.value})

        if len(self.token)<=0:
            self.token.append({'type': Constants.errorToken.value })
        return self.token, self.line


    def characterType(self, char):
        for word in Constants.specialChars.value:
            if char in word['value']:
                return word["name"]

    def replaceSpecialChar(self):
        for word in Constants.specialChars.value:
            self.file = self.file.replace(word["regex"], word["value"])
