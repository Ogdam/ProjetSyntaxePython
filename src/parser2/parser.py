
from .constants import (
    function,
    loop,
    test
)
import re


def lineCuter(tokenList):
    lineList = []
    tList = []
    for token in tokenList:
        if token["type"] != "endOfLine":
            tList.append(token)
        elif token["type"] == "endOfLine":
            lineList.append(tList)
            tList = []
    return lineList


def lineParser(tokenList):
    AST = []
    lineList = lineCuter(tokenList)
    tabulation = 0

    for line in lineList:
        for i in range(0,len(line)-1):
            if line[i]["type"] == "egalite" and line[i+1]["type"] != "egalite":
                AST.append(setAffectation(line, i))
        if line[0]["type"] == "Word":
            if line[0]["value"] == function:
                AST.append(setFunction(line))
    return AST


def setAffectation(line, index):
    value = None
    type = None
    if line[index+1]["type"] == "quote":
        value = getString(line, index+1)
        type = "string"
    else:
        value = line[index+1]['value']
        type = "int"
    create = { 'type': 'variableDeclaration', 'variableName': line[index-1]['value'] }
    affect = { 'type': 'variableAffectation',
               'variableName': 'testNumber',
               'variableValue': { 'type': type, 'value': value } }
    return [create, affect]


def getString(line, index):
    flag = False
    str = ""
    for i in range(index+1, len(line)-1):
        if line[i]['value'] == 'quote':
            break
        else:
            str+=line[i]['value']
    return str

def setFunction(line):
    nom = line[1]["value"]
    variable = []
    flag = False
    for token in line:
        if token['type'] == "openParenthese":
            flag = True
        elif token['type'] == "closeParenthese":
            flag = False
        elif flag and token['type'] != 'comma':
            variable.append(token['value'])
    if re.findall('[a-zA-Z_-]+', nom):
        pass # ajout erreur dans la pile d'érreur nom non valide
    if line[-1]["type"] != 'definitions':
        pass # ajout erreur dans la pile d'érreur pas de :
    return [{'type' : 'functionDeclaration', 'name': nom, 'variable' : variable}]
