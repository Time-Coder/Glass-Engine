# lextab.py. This file automatically created by PLY (version 3.11). Don't edit!
_tabversion = "3.10"
_lextokens = set(
    (
        "CPP_AMPERSAND",
        "CPP_ANDEQUAL",
        "CPP_BAR",
        "CPP_BSLASH",
        "CPP_CHAR",
        "CPP_COLON",
        "CPP_COMMA",
        "CPP_COMMENT1",
        "CPP_COMMENT2",
        "CPP_DEREFERENCE",
        "CPP_DIVIDEEQUAL",
        "CPP_DOT",
        "CPP_DPOUND",
        "CPP_DQUOTE",
        "CPP_EQUAL",
        "CPP_EQUALITY",
        "CPP_EXCLAMATION",
        "CPP_FLOAT",
        "CPP_FSLASH",
        "CPP_GREATER",
        "CPP_GREATEREQUAL",
        "CPP_HAT",
        "CPP_ID",
        "CPP_INEQUALITY",
        "CPP_INTEGER",
        "CPP_LBRACKET",
        "CPP_LCURLY",
        "CPP_LESS",
        "CPP_LESSEQUAL",
        "CPP_LINECONT",
        "CPP_LOGICALAND",
        "CPP_LOGICALOR",
        "CPP_LPAREN",
        "CPP_LSHIFT",
        "CPP_LSHIFTEQUAL",
        "CPP_MINUS",
        "CPP_MINUSEQUAL",
        "CPP_MINUSMINUS",
        "CPP_MULTIPLYEQUAL",
        "CPP_OREQUAL",
        "CPP_PERCENT",
        "CPP_PERCENTEQUAL",
        "CPP_PLUS",
        "CPP_PLUSEQUAL",
        "CPP_PLUSPLUS",
        "CPP_POUND",
        "CPP_QUESTION",
        "CPP_RBRACKET",
        "CPP_RCURLY",
        "CPP_RPAREN",
        "CPP_RSHIFT",
        "CPP_RSHIFTEQUAL",
        "CPP_SEMICOLON",
        "CPP_SQUOTE",
        "CPP_STAR",
        "CPP_STRING",
        "CPP_TILDE",
        "CPP_WS",
        "CPP_XOREQUAL",
    )
)
_lexreflags = 64
_lexliterals = "+-*/%|&~^<>=!?()[]{}.,;:\\'\""
_lexstateinfo = {"INITIAL": "inclusive"}
_lexstatere = {
    "INITIAL": [
        (
            "(?P<t_CPP_WS>([ \\t]+|\\n))|(?P<t_CPP_LINECONT>\\\\[ \\t]*\\n)|(?P<t_CPP_INTEGER>(((((0x)|(0X))[0-9a-fA-F]+)|(\\d+))([uU][lL]|[lL][uU]|[uU]|[lL])?))|(?P<t_CPP_STRING>\\\"([^\\\\\\n]|(\\\\(.|\\n)))*?\\\")|(?P<t_CPP_CHAR>(L)?\\'([^\\\\\\n]|(\\\\(.|\\n)))*?\\')|(?P<t_CPP_COMMENT1>(/\\*(.|\\n)*?\\*/))|(?P<t_CPP_COMMENT2>(//[^\\n]*))|(?P<t_CPP_FLOAT>((\\d+)(\\.\\d+)(e(\\+|-)?(\\d+))?|(\\d+)e(\\+|-)?(\\d+))([lL]|[fF])?)|(?P<t_CPP_ID>[A-Za-z_][\\w_]*)|(?P<t_CPP_LOGICALOR>\\|\\|)|(?P<t_CPP_PLUSPLUS>\\+\\+)|(?P<t_CPP_DPOUND>\\#\\#)|(?P<t_CPP_LSHIFTEQUAL><<=)|(?P<t_CPP_OREQUAL>\\|=)|(?P<t_CPP_PLUSEQUAL>\\+=)|(?P<t_CPP_RSHIFTEQUAL>>>=)|(?P<t_CPP_MULTIPLYEQUAL>\\*=)|(?P<t_CPP_BAR>\\|)|(?P<t_CPP_DIVIDEEQUAL>/=)|(?P<t_CPP_POUND>\\#)|(?P<t_CPP_PERCENTEQUAL>%=)|(?P<t_CPP_DEREFERENCE>->)|(?P<t_CPP_RPAREN>\\))|(?P<t_CPP_ANDEQUAL>&=)|(?P<t_CPP_RBRACKET>\\])|(?P<t_CPP_LPAREN>\\()|(?P<t_CPP_RSHIFT>>>)|(?P<t_CPP_LESSEQUAL><=)|(?P<t_CPP_HAT>\\^)|(?P<t_CPP_LOGICALAND>&&)|(?P<t_CPP_EQUALITY>==)|(?P<t_CPP_GREATEREQUAL>>=)|(?P<t_CPP_BSLASH>\\\\)|(?P<t_CPP_MINUSEQUAL>-=)|(?P<t_CPP_DOT>\\.)|(?P<t_CPP_MINUSMINUS>--)|(?P<t_CPP_LBRACKET>\\[)|(?P<t_CPP_PLUS>\\+)|(?P<t_CPP_XOREQUAL>^=)|(?P<t_CPP_STAR>\\*)|(?P<t_CPP_QUESTION>\\?)|(?P<t_CPP_LSHIFT><<)|(?P<t_CPP_INEQUALITY>!=)|(?P<t_CPP_DQUOTE>\")|(?P<t_CPP_MINUS>-)|(?P<t_CPP_RCURLY>})|(?P<t_CPP_GREATER>>)|(?P<t_CPP_LESS><)|(?P<t_CPP_SQUOTE>')|(?P<t_CPP_EXCLAMATION>!)|(?P<t_CPP_LCURLY>{)|(?P<t_CPP_EQUAL>=)|(?P<t_CPP_FSLASH>/)|(?P<t_CPP_COLON>:)|(?P<t_CPP_AMPERSAND>&)|(?P<t_CPP_COMMA>,)|(?P<t_CPP_TILDE>~)|(?P<t_CPP_SEMICOLON>;)|(?P<t_CPP_PERCENT>%)",
            [
                None,
                ("t_CPP_WS", "CPP_WS"),
                None,
                ("t_CPP_LINECONT", "CPP_LINECONT"),
                ("t_CPP_INTEGER", "CPP_INTEGER"),
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                ("t_CPP_STRING", "CPP_STRING"),
                None,
                None,
                None,
                ("t_CPP_CHAR", "CPP_CHAR"),
                None,
                None,
                None,
                None,
                ("t_CPP_COMMENT1", "CPP_COMMENT1"),
                None,
                None,
                ("t_CPP_COMMENT2", "CPP_COMMENT2"),
                None,
                (None, "CPP_FLOAT"),
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                (None, "CPP_ID"),
                (None, "CPP_LOGICALOR"),
                (None, "CPP_PLUSPLUS"),
                (None, "CPP_DPOUND"),
                (None, "CPP_LSHIFTEQUAL"),
                (None, "CPP_OREQUAL"),
                (None, "CPP_PLUSEQUAL"),
                (None, "CPP_RSHIFTEQUAL"),
                (None, "CPP_MULTIPLYEQUAL"),
                (None, "CPP_BAR"),
                (None, "CPP_DIVIDEEQUAL"),
                (None, "CPP_POUND"),
                (None, "CPP_PERCENTEQUAL"),
                (None, "CPP_DEREFERENCE"),
                (None, "CPP_RPAREN"),
                (None, "CPP_ANDEQUAL"),
                (None, "CPP_RBRACKET"),
                (None, "CPP_LPAREN"),
                (None, "CPP_RSHIFT"),
                (None, "CPP_LESSEQUAL"),
                (None, "CPP_HAT"),
                (None, "CPP_LOGICALAND"),
                (None, "CPP_EQUALITY"),
                (None, "CPP_GREATEREQUAL"),
                (None, "CPP_BSLASH"),
                (None, "CPP_MINUSEQUAL"),
                (None, "CPP_DOT"),
                (None, "CPP_MINUSMINUS"),
                (None, "CPP_LBRACKET"),
                (None, "CPP_PLUS"),
                (None, "CPP_XOREQUAL"),
                (None, "CPP_STAR"),
                (None, "CPP_QUESTION"),
                (None, "CPP_LSHIFT"),
                (None, "CPP_INEQUALITY"),
                (None, "CPP_DQUOTE"),
                (None, "CPP_MINUS"),
                (None, "CPP_RCURLY"),
                (None, "CPP_GREATER"),
                (None, "CPP_LESS"),
                (None, "CPP_SQUOTE"),
                (None, "CPP_EXCLAMATION"),
                (None, "CPP_LCURLY"),
                (None, "CPP_EQUAL"),
                (None, "CPP_FSLASH"),
                (None, "CPP_COLON"),
                (None, "CPP_AMPERSAND"),
                (None, "CPP_COMMA"),
                (None, "CPP_TILDE"),
                (None, "CPP_SEMICOLON"),
                (None, "CPP_PERCENT"),
            ],
        )
    ]
}
_lexstateignore = {"INITIAL": ""}
_lexstateerrorf = {"INITIAL": "t_error"}
_lexstateeoff = {}
