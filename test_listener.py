#!/usr/bin/env python3

import os, glob
from typing import Callable

from antlr4 import InputStream, CommonTokenStream, ParseTreeWalker, ParserRuleContext

from grammar.PlSqlLexer import PlSqlLexer
from grammar.PlSqlParserListener import PlSqlParserListener
from grammar.PlSqlParser import PlSqlParser

def lalign(text: str, width: int, fillchar: str = ' ') -> str:
	return text[:width].ljust(width, fillchar)

def ralign(text: str, width: int, fillchar: str = ' ') -> str:
	return text[:width].rjust(width, fillchar)

class PlSqlParserListenerBase(PlSqlParserListener):
	def __init__(self, parser: PlSqlParser):
		self.parser: PlSqlParser = parser

class PlSqlParserListenerDebug(PlSqlParserListenerBase):
	def __init__(self, parser: PlSqlParser):
		super().__init__(parser)
		self.line(indent=0, ruleName='ruleName', id='id', start='start')
		self.line(indent=0, ruleName='', id='', start='', fillchar = '-')
	
	def line(self, indent: int, ruleName: str, id: str, start: str, fillchar: str = ' '):
		text = ''

		text += lalign((fillchar * indent) + ruleName, 60, fillchar) + ' '
		text += lalign(id, 30, fillchar) + ' '
		text += lalign(start, 30, fillchar)

		print(text)

	def enterEveryRule(self, ctx: ParserRuleContext):
		ruleIndex = ctx.getRuleIndex()
		ruleNames = self.parser.ruleNames
		ruleName = ruleNames[ruleIndex]
		id = ''
		if ruleName in ('regular_id', 'native_datatype_element'):
			id = ctx.getText()

		self.line(indent=ctx.depth() - 1, ruleName=ruleName, id=id, start=str(ctx.start))

	def exitEveryRule(self, ctx: ParserRuleContext):
		pass

class PlSqlParserListenerCustom(PlSqlParserListenerBase):
	def __init__(self, parser: PlSqlParser):
		super().__init__(parser)

	def line(self, title: str):
		print(title)

	def enterSql_script(self, ctx: PlSqlParser.Sql_scriptContext):
		self.line('enterSql_script')

	def exitSql_script(self, ctx: PlSqlParser.Sql_scriptContext):
		self.line('exitSql_script')

	def enterCreate_function_body(self, ctx: PlSqlParser.Create_function_bodyContext):
		self.line('enterCreate_function_body')

def parse(content: str, listenerFunction: Callable[[PlSqlParser], PlSqlParserListenerBase]):
	print(f'\n{"*" * 80}\n{content}\n{"*" * 80}\n')

	# Convert the file into a character stream
	input_stream = InputStream(content)
	
	# Create the lexer
	lexer = PlSqlLexer(input_stream)
	
	# Convert the lexer output into a token stream
	token_stream = CommonTokenStream(lexer)
	
	# Create the parser
	parser = PlSqlParser(token_stream)

	# Create the listener
	listener = listenerFunction(parser)

	# Create the walker
	walker = ParseTreeWalker()
	walker.walk(listener, parser.sql_script())

def main():
	files = glob.glob(os.path.join("tests", "*.sql"))

	for file in files:
		with open(file, "r") as plsql_file:
			parse(content=plsql_file.read(), listenerFunction=PlSqlParserListenerCustom)

if __name__ == "__main__":
	main()
