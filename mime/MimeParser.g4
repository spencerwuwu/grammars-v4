parser grammar MimeParser;

options {
    tokenVocab = MimeLexer;
}

// Top-level MIME message with flexible structure
mimeMessage
    : simpleBody                                    // Just content
    | headersOnly                                   // Headers without body
    | headersBody                                   // Headers + simple body
    | multipart                                     // Multipart message
    ;

// Headers only (no body separator)
headersOnly
    : header+ EOF
    ;

blankLine
    : (CRLF | LF)
    ;

// Headers followed by body
headersBody
    : header+ blankLine body
    ;

// Simple body without headers
simpleBody
    : body
    ;

// Multipart structure
multipart
    : header+ (CRLF | LF)
      preamble?
      part+
      BOUNDARY_END (CRLF | LF)?
      epilogue?
    ;

// Generic header structure
header
    : headerName COLON WSP* headerValue (CRLF | LF)
    ;

headerName
    : WORD (UNDERLINE WORD)*
    ;

// Header value (fixed empty string issue)
headerValue
    : headerValuePart+ (WSP headerValuePart*)*
    | /* empty */
    ;

headerValuePart
    : WORD
    | SPECIAL_TOKEN
    | QUOTED_STRING
    | VERSION
    | DIGITS
    | mediaType
    | parameter
    | COMMENT
    | SLASH | SEMICOLON | COMMA | EQUALS
    ;

// Media type parsing
mediaType
    : WORD SLASH WORD
    ;

// Parameter parsing
parameter
    : WORD EQUALS (WORD | SPECIAL_TOKEN | QUOTED_STRING | DIGITS)
    ;

// Multipart components
preamble
    : bodyContent
    ;

part
    : BOUNDARY_START (CRLF | LF)
      header*
      (CRLF | LF)?
      bodyContent?
    ;

epilogue
    : bodyContent
    ;

// Body content
body
    : bodyContent
    ;

bodyContent
    : bodyLine+
    ;

bodyLine
    : contentData? (CRLF | LF)
    ;

contentData
    : (WSP | WORD | DIGITS | SPECIAL_TOKEN | DOUBLE_DASH | CONTENT_CHAR)+
    ;
