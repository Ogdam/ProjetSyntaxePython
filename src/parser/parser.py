from tokenizer.constants import (
    typeWord,
    typeNumber
)
from .expressionsFactory import create
from .constantes import expressionAffectation

def ast(tokens):
    AST = []
    for i in range(len(tokens)):
        expression = None
        #
        if (tokens[i].type == typeWord) :
            #if dans mots clés -> fct associé
            #else
            if tokens[i+1].type=="affectation" :
                expression=create(expressionAffectation, tokens, i)
                #si affectation d'un nombre
                if expression.variableValue.type == typeNumber :
                    i=i+1
                #si affectation d'un string on reprend l'analyse après la fermeture des guillements.
                else :
                    i= expression.variableValue.end
            elif tokens[i+1].type!="endOfLine" :
                raise Exception("erreur sur l'affectation de cette variable")

        if (expression):
            AST.append(expression)
        else:
            AST.append(tokens[i])

    return AST
