grammar scheme;

program: (functiondef|constdef)* EOF;

functiondef: OPEN 'define' OPEN IDENTIFIER IDENTIFIER* CLOSE expression+ CLOSE;

constdef: OPEN 'define' IDENTIFIER value CLOSE;

expression: IDENTIFIER | value | letexpr | ifexpr | condexpr | aritmexpr | logicfunc | logicop | listfunc | iofunc | trucada;

letexpr: OPEN 'let' OPEN letvar+ CLOSE expression+ CLOSE;
letvar: OPEN IDENTIFIER expression CLOSE;

ifexpr: OPEN 'if' expression expression expression CLOSE;

condexpr: OPEN 'cond' (condi)+ CLOSE;
condi: OPEN expression expression+ CLOSE;

aritmexpr: OPEN aoperator expression expression CLOSE;
aoperator: '+' | '-' | '*' | '/' | 'mod';

logicfunc: OPEN logicdoor expression expression CLOSE | OPEN 'not' expression CLOSE;
logicdoor: 'and' | 'or';

logicop: OPEN loperator expression expression CLOSE;
loperator: '<' | '>' | '=' | '<>' | '<=' | '>=';

listfunc: OPEN listf expression CLOSE;
listf: 'car' | 'cdr' | 'null?' | ('cons' expression);

iofunc: OPEN 'newline' CLOSE | OPEN 'read' CLOSE | OPEN 'display' expression CLOSE;

trucada: OPEN IDENTIFIER expression* CLOSE;

value: BOOLEAN | NUMBER | STRING | llista;
llista: '\'' OPEN value* CLOSE;

//Tokens
OPEN: '(';
CLOSE: ')';
BOOLEAN: '#t' | '#f';
NUMBER: [0-9]+;
STRING: '"' ~[*"\r\n]* '"';
IDENTIFIER: [a-zA-Z] [-a-zA-Z0-9?_]*;
WS: [ \t\r\n]+ -> skip;
COMENTARI: ';' ~[\r\n]* -> skip;
