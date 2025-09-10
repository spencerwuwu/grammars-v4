lexer grammar JSONLexer;

QUOTE:      '"';
BACKSLASH:  '\\';
PLUS:       '+';
MINUS:      '-';
LBRACE:     '{';
RBRACE:     '}';
LBRACK:     '[';
RBRACK:     ']';
COMMA:      ',';
COLON:      ':';
DOT:        '.';


TRUE:       'true';
FALSE:      'false';
NULL:       'null';


E:          [eE];
U:          'u';
ZERO:       '0';
DIGIT19:    [1-9];

HEXALPHA_REST:   [a-dA-D] | [fF];

ESC:        BACKSLASH (["/bfnrt] | BACKSLASH)
    ;

WS
    : [ \t\n\r]+ -> skip
    ;

SAFECODEPOINT
    : ~ ["\\\u0000-\u001F]
    ;

