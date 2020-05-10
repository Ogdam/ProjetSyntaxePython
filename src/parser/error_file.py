import re

class ErrorList():

    def __init__(self, line):
        self.errorList = []
        self.lineNumber = line

    def testCamelCaseErrorName(self, name, line):
        if not re.match('[a-zA-Z]', name):
            self.errorList.append("line {} : {} doen't respect the camel case".format(line, name))
            return False
        return True

    def errorTabulationsManquante(self, line):
        self.errorList.append("line {} : Tabulation missing".format(line))

    def errorMissingColon(self, line):
        self.errorList.append("line {} : missing colon ':' ".format(line))

    def errorMissingParenthese(self, line):
        self.errorList.append("line {} : missing Parenthese ".format(line))

    def errorEndBlockDeclaration(self,line):
        self.errorList.append("line {} : can't have something after the end of the block declaration ':' ".format(line))

    def errorConditionOrder(self,line):
        self.errorList.append("line {} : les conditions doivent commencer par un if si il n'y a pas de conditions avant ou si c'était un else ".format(line))

    def errorAffectation(self,line):
        self.errorList.append("line {} : wrong syntax in this affectation ".format(line))

    def errorElse(self,line):
        self.errorList.append("line {} : ne rien mettre entre un else et le ':' ".format(line))

    def errorBoucles(self,line):
        self.errorList.append("line {} : erreur de syntaxe dans la déclaration de la boucle ".format(line))

    def variableNonUse(self, name, line):
        self.errorList.append("line {} : variable {} non use".format(line, name))

    def errorMissingQuote(self, line):
        self.errorList.append("line {} : quote missing".format(line))

    def calculNote(self):
        return (((self.lineNumber*2)-len(self.errorList))/(self.lineNumber*2)) * 5

    def errorFileTooLong(self):
        self.errorList.append("File over 200 lines")

    def getErrorList(self):
        return self.errorList
