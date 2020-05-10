from .constants import Constants
import re
from .error_file import ErrorList


def countIndentation(line):
    cpt=0
    for i in line:
        if i.get('type') == 'space':
            cpt=cpt+1
        else:
            break
    return cpt

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

def finBlock (block):
    if block.get('type')=='functionDeclaration' :
         return {'type' : 'endFunction'  , 'name' : block.get('name') , 'variable': block.get('variable'), 'indentation':block.get('indentation')}
    elif block.get('type') in Constants.test.value :
        return {'type' : 'endCondition'  , 'conditionType' : block.get('type') , 'boolean': block.get('boolean'), 'indentation':block.get('indentation')}
    elif block.get('type') in Constants.loop.value :
        if block.get('type')=='for':
            return {'type' : 'endFor'  , 'name' : block.get('name') , 'element': block.get('element'), 'ensemble':block.get('ensemble'), 'indentation':block.get('indentation')}
        else:
            return {'type' : 'endWhile'  , 'name' : block.get('name') , 'condition': block.get('condition'), 'indentation':block.get('indentation')}

class Parser():

    def __init__(self, tokenList, fileLength):
        self.lineList = lineCuter(tokenList)
        self.listError = ErrorList(fileLength)

    def lineParser(self):
        AST = []
        listBlocIndentation = [0]*25
        maxTabulation = 0 #désigne la tabulation que peut au maximum avoir la ligne
        needTabulation=0 #désigne la tabulation que doit avoir la prochaine ligne (si on a eu un if par exemple)


        for index, line in enumerate(self.lineList):
            nbIndentation= countIndentation(line)
            ancienBlock=0
            #tests tabulation
            if needTabulation!=0 :
                maxTabulation=needTabulation
            if nbIndentation>maxTabulation or (needTabulation!=0 and nbIndentation!=needTabulation) or nbIndentation%4!=0 :

                self.listError.errorTabulationsManquante(index+1)#ajouter différents messages selon les cas?
            for numberBloc in range(len(listBlocIndentation)-1,-1,-1) :
                if listBlocIndentation[numberBloc]!=0:
                    if nbIndentation <= numberBloc*4 :
                        if nbIndentation==numberBloc*4 : #sert pour les if/elif/else
                            ancienBlock=listBlocIndentation[numberBloc]
                        AST.append(finBlock( listBlocIndentation[numberBloc]))
                        listBlocIndentation[numberBloc] = 0
                        maxTabulation = numberBloc*4
                    else :
                        break
            needTabulation=0

            #read line
            noMoreElements= False #bool servant à tester si il reste des chose ecrite après un  ' : '
            i=nbIndentation
            while i < len(line):
                flag=False
                if noMoreElements:
                    print(i)
                    print(line)
                    print(len(line))
                    self.listError.errorEndBlockDeclaration(index+1)
                    break
                if line[i]["type"] == "Word":
                    #déclaration de fonction
                    if line[i]["value"] == Constants.function.value and i==nbIndentation:
                        tempo = self.setFunction(line, index, nbIndentation)
                        AST.append(tempo[0])
                        listBlocIndentation[i//4]=tempo[0]
                        needTabulation= i+4
                        noMoreElements=True
                        flag=True
                        i = i + tempo[1]
                    #si c'est une boucle:
                    elif line[i]["value"] in Constants.loop.value and i==nbIndentation:
                        tempo = self.setBoucle(line,index, i)
                        AST.append(tempo[0])
                        listBlocIndentation[i//4]=tempo[0]
                        needTabulation= i+4
                        noMoreElements=True
                        flag=True
                        i = i + tempo[1]
                    #si c'est une condition:
                    elif line[i]["value"] in Constants.test.value and i==nbIndentation:
                        rightCondition=True
                        if ancienBlock==0 or (ancienBlock["type"]!="elif" and ancienBlock["type"]!="if") :
                            if line[i]["value"]!="if":
                                rightCondition=False
                                self.listError.errorConditionOrder(index+1)
                                maxTabulation = maxTabulation+4
                                break
                        if rightCondition:
                            tempo= self.setCondition(line,index,i)
                            AST.append(tempo[0])
                            listBlocIndentation[i//4]=tempo[0]
                            needTabulation= i+4
                            noMoreElements=True
                            flag=True
                            i = i + tempo[1]
                    #si c'est une affectation
                    else :
                        if len(line)>i+1 and line[i+1]["type"] == "affectation" :
                            create, affect, end = self.setAffectation(index, line, i+1)
                            if create is None or affect is None:
                                break
                            AST.append(create)
                            AST.append(affect)
                            flag=True
                            #si affectation d'un nombre alors
                            if end == 0:
                                i=i+3
                            #si affectation d'un string on reprend l'analyse après la fermeture des guillements.
                            else:
                                i=  i + end +1
                            noMoreElements=True
                        #elif on a rien apres le égal
                        elif i<len(line)-1 : #après un word en début de ligne c'est soit un égal soit une fin de ligne sinon faux
                            egaliter = self.setTest(index, line, i+1)
                            AST.append(egaliter)
                            break
                if not flag:#cas poubelle , on ajoute juste à la suite
                     AST.append(line[i])
                    # print("on a un element (Han)solo sur une ligne : "+ line[i]['type'])
                     i=i+1
            #fin while
        #fin for + ferme tout les blocs si on est arrivé à la fin de la dernière liste
        if index==len(self.lineList)-1:
            for numberBloc in range(len(listBlocIndentation)-1,-1,-1) :
                if listBlocIndentation[numberBloc]!=0:
                    AST.append(finBlock( listBlocIndentation[numberBloc]))
        return AST, self.listError


    def setTest(self, indexLine, line, index):
        return {'type' : line[index]['type'], "var" :[ line[index-1]['value'], line[index+1]['value']] }

    def setAffectation(self, indexLine, line, index):
        value = None
        type = None
        end=0
        tempo=""
        self.listError.testCamelCaseErrorName(line[index-1]['value'], indexLine+1)
        if line[index+1]["type"] == "quote":
            tempo = self.getString(line, index+1, indexLine)
            if tempo != None :
                value = tempo[0]
                end=tempo[1]+1
                type = "Word"
        elif line[index+1]["type"] == "openCrochet":
            tempo= self.getList(line, indexLine ,index+1)
            if tempo != None :
                value = tempo[0]
                end=tempo[1]+1
                type = "List"
        elif line[index+1]["type"] == "Number":
            value = line[index+1]['value']
            type = "Number"
        if tempo != None:
            create = { 'type': 'variableDeclaration', 'variableName': line[index-1]['value'] }
            affect = { 'type': 'variableAffectation',
                       'variableName': line[index-1]['value'],
                       'variableValue': { 'type': type, 'value': value }}
            return [create, affect,end]
        return None, None

    def getString(self, line, index, indexLine):
        flag = False
        str = ""
        cpt=2
        for i in range(index+1, len(line)):
            if line[i]['type'] == 'quote':
                flag=True
                break
            else:
                str+=line[i]['value']
                cpt=cpt+1
        if flag:
            return [str,cpt]
        else:
            self.listError.errorMissingQuote(indexLine+1)
            return [str,cpt]


    def getList(self, line , indexLine, i):
        list=[]
        cpt=2
        commaFlag=True
        errorComa=False
        errorSyntaxFlag=True
        element=''
        for k in range (i+1,len(line)):
            if line[k]['type']=='closeCrochet':
                list.append(element)
                errorSyntaxFlag=False
                break
            elif line[k]['type']=='comma':
                if commaFlag:
                    errorComa=True
                else:
                    list.append(element)
                    element=''
                    commaFlag=True
            else:
                element= element + str(line[k]['value'])
                commaFlag=False
            cpt=cpt+1
        if errorSyntaxFlag or errorComa:
            self.listError.errorListAffectation(indexLine+1)
        return [list,cpt]


    def setFunction(self, line, index ,i):
        functionName=''
        variable = []
        flag = False
        numberTokenSeen=5
        errorSyntaxe=True
        if line[i]['type']=='Word' and line[i]['value']=='def' and len(line)>i+2 :
            if line[i+1]['type']=='Word':
                functionName = line[i+1]['value']
                if line[i+2]['type']=='openParenthese':
                    for k in range(i+3,len(line)):
                        if line[k]['type'] == "closeParenthese":
                            if len(line)>k+1 :
                                if line[k+1]['type']=='definitions':
                                    errorSyntaxe=False
                            break
                        elif line[k]['type'] != 'comma':
                            variable.append(line[k]['value'])
                            numberTokenSeen = numberTokenSeen + 1
                        elif line[k]['type'] == 'comma':
                            numberTokenSeen = numberTokenSeen + 1
        if errorSyntaxe:
            if line[-1]['type']!='definitions':
                self.listError.errorMissingColon(index+1)
            else:
                self.listError.errorDefFunction(index+1)
            return [{'type' : 'functionDeclaration', 'name': functionName, 'variable' : variable ,"indentation": i},len(line)]
        self.listError.testCamelCaseErrorName(functionName, index+1)
        return [{'type' : 'functionDeclaration', 'name': functionName, 'variable' : variable ,"indentation": i},numberTokenSeen]


    def setCondition (self, line, index, i):
        booleanString = ""
        flag=False
        cpt=2
        if line[i]["value"]== 'if' or line[i]["value"]== 'elif':
            for k in range(i+1, len(line)):
                if line[k]["type"] != 'definitions':
                    if line[k]['type'] not in ['Word', 'Number']:
                        for test in Constants.testChar.value:
                            if line[k]['type'] == test['name']:
                                booleanString+=test['regex']
                    else:
                        booleanString= booleanString+line[k]['value']
                    cpt=cpt+1
                else:
                    flag=True
                    break
        else :
            if len(line)>i+1 and line[i+1]["type"] == 'definitions':
                flag=True
            else:
                self.listError.errorElse(index+1)
        if not flag :
            self.listError.errorMissingColon(index+1)
        return [{'type' : line[i]["value"], 'boolean' : booleanString, 'indentation' : i},cpt]


    def setBoucle (self, line , index , i):
        errorSyntaxe=True
        element=""
        ensemble=''
        cpt=0
        booleanString=''
        if line[i]['type']=='Word' and line[i]['value']=='for' and len(line)>i+3:
            cpt=5
            if line[i+1]['type']=='Word':
                element=line[i+1]['value']
                if line[i+2]['type']=='Word' and line[i+2]['value']=='in' :
                    for k in range(i+3,len(line)):
                        if line[k]['type']=='definitions':
                            if(k!=i+3):
                                errorSyntaxe=False
                                break
                            else:
                                break
                        else:
                            if line[k]['type'] not in ['Word', 'Number']:
                                for test in Constants.testChar.value:
                                    if line[k]['type'] == test['name']:
                                        booleanString+=test['regex']
                            else:
                                ensemble+=line[k]['value']
                            cpt=cpt+1
            cpt=len(line)
        elif line[i]['type']=='Word' and line[i]['value']=='while' and len(line)>i+2:
            cpt=2
            for k in range(i+1, len(line)):
                if line[k]["type"] != 'definitions':
                    if line[k]['type'] not in ['Word', 'Number']:
                        for test in Constants.testChar.value:
                            if line[k]['type'] == test['name']:
                                booleanString+=test['regex']
                    else:
                        booleanString= booleanString+line[k]['value']
                    cpt=cpt+1
                else:
                    errorSyntaxe=False
                    break
            cpt=len(line)
        if errorSyntaxe:
            self.listError.errorBoucles(index+1)
        if line[i]['value']=='for':
            return [{'type':'for', 'element':element, 'ensemble':ensemble,'indentation':i},cpt]
        else:
            return [{'type':'while', 'condition':booleanString,'indentation':i},cpt]
