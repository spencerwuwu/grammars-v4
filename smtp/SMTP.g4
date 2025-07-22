
grammar SMTP;

// Entry point
session         : command;

// === SMTP Commands ===
command         : ( helo | ehlo )
                 mailFrom
                 rcptTo+
                 dataCmd
                 quit
                ;

helo            : 'HELO' SP domain CRLF;
ehlo            : 'EHLO' SP domain CRLF;
mailFrom        : 'MAIL FROM:' reversePath CRLF;
rcptTo          : 'RCPT TO:' forwardPath CRLF;
dataCmd         : 'DATA' CRLF dataBody '.' CRLF;

quit            : 'QUIT' CRLF;


// === Paths ===
reversePath     : '<' path? '>';
forwardPath     : '<' path '>';
path            : a_d_l? ':'? mailbox;
// optional source route: @domain,@domain,...
a_d_l           : atDomain (',' atDomain)* ;
atDomain        : '@' domain ;

mailbox         : localPart '@' domain;


// === Message Data ===
dataBody        : (dataLine CRLF)*;
dataLine       : ~'.'+;  // line must not start with single '.'


// === Identifiers ===
domain          : subDomain ('.' subDomain)*;
subDomain       : ALPHA (ALPHA | DIGIT | '-')*;

// === Local-part ===
 localPart
    : dotString
    | quotedString
    ;

// dot-string = atom *("." atom)
dotString
    : atom ('.' atom)*
    ;

atom : (ALPHA | DIGIT | ATEXT_PUN )+;

// quoted-string = DQUOTE *(qtext / quoted-pair) DQUOTE
quotedString
    : DQUOTE (qtext | quotedPair)* DQUOTE
    ;

qtext
    : QTEXT
    | ALPHA | DIGIT | ATEXT_PUN
    | '<' | '>' | '@' | '.'
    | ':'
    | CRLF
    | SP
    ;

quotedPair
    : '\\' .
    ;


// === LEXER RULES ===
CRLF            : '\r\n';
SP              : ' ';
ALPHA           : [a-zA-Z];
DIGIT           : [0-9];
ATEXT_PUN       : [!#$%&'*+/=?^_`{|}~-];

DQUOTE      : '"';
QTEXT       : ~["\\\r\n];

//WS              : [ \t]+ -> skip;

