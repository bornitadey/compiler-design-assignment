%{
#include <stdio.h>
%}
%option noyywrap
DIGIT  [0-9]
LETTER [a-zA-Z_]
%%
"int"|"float"|"char"|"void"|"if"|"else"|"while"|"for"|"return"  { printf("KEYWORD\t\t%s\n", yytext); }
{LETTER}({LETTER}|{DIGIT})*     { printf("IDENTIFIER\t%s\n", yytext); }
{DIGIT}+(\.{DIGIT}+)?           { printf("NUMBER\t\t%s\n", yytext); }
\"[^\"\n]*\"                    { printf("STRING\t\t%s\n", yytext); }
"//".*                          { /* single-line comment */ }
"/*"([^*]|\*+[^*/])*\*+"/"      { /* multi-line comment */ }
"=="|"!="|"<="|">="|"&&"|"||"|"++"|"--"  { printf("OPERATOR\t%s\n", yytext); }
[+\-*/=<>!%]                    { printf("OPERATOR\t%s\n", yytext); }
[(){}\[\];,]                    { printf("DELIMITER\t%s\n", yytext); }
[ \t\n]+                        { /* skip whitespace */ }
.                               { printf("UNKNOWN\t\t%s\n", yytext); }
%%
int main(int argc, char *argv[]) {
    if (argc > 1) yyin = fopen(argv[1], "r");
    yylex();
    return 0;
}