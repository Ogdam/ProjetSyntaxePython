import tokenizer.constants as constToken
import parser.constantes as constParser
import helper

def create(type,tokens,start):
    return {
        constParser.expressionMethodCall : objectMethodCall(tokens, start),
        constParser.expressionAffectation : variableAffectation(tokens, start)
        }[type]


def objectMethodCall(tokens, start):
    return

def variableAffectation (tokens, start) :
    variableName=tokens[start]
    if tokens[start+2].type == constToken.typeNumber:
        variableValue= tokens[start+2]
    #elif tokens[start+2].type == constToken.typeWord : (c'est un appel de fonction ou une autre variable)
    elif tokens[start+2].type == constToken.symboleQuotationMark :
        variableValue= helper.searchString(tokens, start+2);
    return {type: constParser.expressionAffectation, variableName: variableName, variableValue: variableValue};
