import parser.constantes as constParser
import tokenizer.constants as constToken

def searchString(tokens, start):
    string=[]
    findend=False
    end=0
    for i in range(start+1,len(tokens)):
        if tokens[i].type == constToken.symboleQuotationMark :
            findend= True
            end= i
            break
        elif tokens[i].type =="endOfLine":
            raise Exception("pas de fermeture de la quote mark avant la fin de la ligne")
        else :
            string.append(tokens[i].value)
    if findend :
        raise Exception("pas de fermeture de la quote mark avant la fin du fichier")
    else :
        return {'type':constParser.typeString, 'value': "".join(string), start: start, end: end}
