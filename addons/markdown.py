# MIT License
# 
# Copyright (c) 2022 Dr John Vidler
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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