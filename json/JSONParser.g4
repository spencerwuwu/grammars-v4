parser grammar JSONParser;

options {
    tokenVocab = JSONLexer;
}

json
    : value EOF
    ;

obj
    : LBRACE pair (COMMA (obj | pair))* RBRACE
    | LBRACE RBRACE
    ;

pair
    : string COLON value
    ;

arr
    : LBRACK value (COMMA value)* RBRACK
    | LBRACK RBRACK
    ;

value
    : string
    | number
    | obj
    | arr
    | TRUE
    | FALSE
    | NULL
    ;

string
    : QUOTE
    (ESC | SAFECODEPOINT
         | E | U
         | HEXALPHA_REST | ZERO | DIGIT19
         | BACKSLASH
         | MINUS | PLUS | DOT
         | COMMA | COLON | LBRACE | RBRACE | LBRACK | RBRACK
         | WS
    )* QUOTE
    ;

hex
    : E | HEXALPHA_REST | ZERO | DIGIT19
    ;

unicode
    : BACKSLASH U hex hex hex hex
    ;

int
    : ZERO | (DIGIT19 int*)
    ;

number
    : MINUS? int (DOT (DIGIT19 | ZERO)+)? exp?
    ;

exp
    : E (PLUS|MINUS)? (ZERO | DIGIT19)+
    ;

