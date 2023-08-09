#!/usr/bin/env python3

from antlr4 import *
from grammar.PlSqlLexer import PlSqlLexer
from grammar.PlSqlParser import PlSqlParser
#from grammar.PlSqlParserListener import PlSqlParserListener

input = InputStream("-- select\nselect * from dual;")
lexer = PlSqlLexer(input)

tokens = CommonTokenStream(lexer)
parser = PlSqlParser(tokens)
tree = parser.sql_script()

print (tree.toStringTree(recog=parser));
