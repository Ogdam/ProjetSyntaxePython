from enum import Enum


class Constants(Enum):
    function = 'def'
    loop = ('for', 'while')
    test = ('if', 'else', 'elif')

    testChar = [
        {"name":"Equal"                , "regex": "=="  },
        {"name":"InfOrEqual"           , "regex": ">="  },
        {"name":"SupOrEqual"           , "regex": "<="  },
        {"name":"Different"            , "regex": "!="  },
        {"name":"affectation"          , "regex": "="   },
        {"name":"inferieur"            , "regex": ">"   },
        {"name":"superieur"            , "regex": "<"   }
    ]
