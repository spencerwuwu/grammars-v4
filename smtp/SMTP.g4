
grammar SMTP;

// Entry point
session         : command;

// === SMTP Commands ===
command         : ( helo | ehlo )
                 mailFrom
                 quit
                ;

helo            : 'HELO' SP domain CRLF;
ehlo            : 'EHLO' SP domain CRLF;
mailFrom        : 'MAIL FROM:' reversePath CRLF;

quit            : 'QUIT' CRLF;


// === Paths ===
reversePath     : '<' path? '>';
forwardPath     : '<' path '>';
path            : mailbox;
mailbox         : localPart '@' domain;


// === Message Data ===


// === Identifiers ===
domain          : subDomain ('.' subDomain)*;
subDomain       : LETTER (LETTER | DIGIT | '-')*;
//localPart       : WORD ('.' WORD)*;


// === LEXER RULES ===
CRLF            : '\r\n';
SP              : ' ';
LETTER          : [a-zA-Z];
DIGIT           : [0-9];
CHAR            : LETTER
                | DIGIT
                | [!#$%&'*+/=?^_`{|}~-]
                ;
//WORD            : CHAR +;

WS              : [ \t]+ -> skip;

