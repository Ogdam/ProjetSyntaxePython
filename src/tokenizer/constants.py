
specialChars = [
    { "value": ' *=* '  ,  "name":"egalite"              , "regex": "="  },
    { "value": ' *<* '  ,  "name":"inferieur"            , "regex": ">"  },
    { "value": ' *>* '  ,  "name":"superieur"            , "regex": "<"  },
    { "value": ' *\v* ' ,  "name":"lineReturn"           , "regex": "\v" },
    { "value": ' *\t* ' ,  "name":"tabulation"           , "regex": "\t" },
    { "value": ' *:* '  ,  "name":"definitions"          , "regex": ":"  },
    { "value": ' *(* '  ,  "name":"openParenthese"       , "regex": "("  },
    { "value": ' *)* '  ,  "name":"closeParenthese"      , "regex": ")"  },
    { "value": ' *{* '  ,  "name":"openAcolade"          , "regex": "{"  },
    { "value": ' *}* '  ,  "name":"closeAcolade"         , "regex": "}"  },
    { "value": ' *[* '  ,  "name":"openCrochet"          , "regex": "["  },
    { "value": ' *]* '  ,  "name":"closeCrochet"         , "regex": "]"  },
    { "value": ' *,* '  ,  "name":"comma"                , "regex": ","  },
    { "value": ' *\"* '  ,  "name":"quote"               , "regex": '\"'  }
]

typeWord = "Word"
typeNumber = "Number"
endOfLine = "endOfLine"

errorToken = "No token found in file"
