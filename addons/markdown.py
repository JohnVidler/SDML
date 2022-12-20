import re
from SDMLParser import Parser, Directive
from Lexer import Token, TokenType

lexerFunc = None

def lex_findPrefixTokens( lexer, line: str ):
    line = line.lstrip() # OK, drop any whitespace, we don't care for such things anymore (post-scope)

    titleMatch = re.search( '^(#+)[^#]', line )
    if titleMatch:
        titleDepth = len( titleMatch.group(1) )
        lexer.buffer.append( Token( lexer.scope, Directive.TITLE, TokenType.DIRECTIVE, lexer.inputLine ) )
        lexer.buffer.append( Token( lexer.scope+1, "depth",         TokenType.ARGUMENT,  lexer.inputLine ) )
        lexer.buffer.append( Token( lexer.scope+1, str(titleDepth), TokenType.TEXT,      lexer.inputLine ) )
        lexer.buffer.append( Token( lexer.scope+1, "value",         TokenType.ARGUMENT,  lexer.inputLine ) )
        # The next set of tokens should be the title proper, so we've set the parser up to deal with it here

        # Drop the '#' string, so it doesn't get emitted with the title...
        line = line[titleDepth:]

    return line

def bind( parser: Parser ):
    lexer = parser.lexer

    lexer.setStage( 25, lex_findPrefixTokens )

def unbind( parser: Parser ):
    lexer = parser.lexer
    lexer.clearStage( 25, lex_findPrefixTokens )