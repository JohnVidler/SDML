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
import os
from DataStructures import SparseList
from enum import Enum

ENCODING = os.getenv("SDML_ENCODING", 'utf-8' )

class TokenType(Enum):
    TEXT = 0
    BREAK = 1
    DIRECTIVE = 2
    ARGUMENT = 3

class Token:
    scope = None
    type = None
    value = None
    line: int = -1

    def __init__( self, scope, value, type = TokenType.TEXT, line: int = None ) -> None:
        self.scope = scope
        self.type = type
        self.value = value
        self.line = line
    
    def __str__(self) -> str:
        return F"[Token line={self.line}, type={self.type}, scope={self.scope}, value={self.value}]"
    
    def isChildOf( self, parent ):
        return parent.scope == self.scope-1
    
    def isParentOf( self, child ):
        return child.scope == self.scope+1

def lex_rStrip( lexer, line: str ):
    return line.rstrip() # Drop the trailing \n, plus any additional whitespace

def lex_blankBreaks( lexer, line: str ):
    if len(line) == 0:
        lexer.buffer.append( Token( lexer.scope, None, type=TokenType.BREAK, line=lexer.inputLine ) )
    return line

def lex_handleScope( lexer, line: str ):
    lexer.scope = 0
    scopePrefix = re.search( '^(\s+)', line )
    if scopePrefix != None:
        if lexer.scopeStep == 0:
            print( F"First scoped block, using {len(scopePrefix.group(1))} spaces as our scope step size" )
            lexer.scopeStep = len(scopePrefix.group(1))
        lexer.scope = int(len(scopePrefix.group(1)) / lexer.scopeStep)
    return line

def lex_handleDirective( lexer, line: str ):
    directiveMatch = re.search( '^\W*\.\.([^:]+):', line )
    if directiveMatch:
        lexer.buffer.append( Token( lexer.scope, directiveMatch.group(1), type = TokenType.DIRECTIVE, line = lexer.inputLine ) )

        # Consume this from the input
        line = line[ len(directiveMatch.group(0)): ].lstrip()
    return line

def lex_handleText( lexer, line: str ):
    for word in line.split():
        lexer.buffer.append( Token( lexer.scope, word, type = TokenType.TEXT, line = lexer.inputLine ) )    
    return line

class Lexer:
    input = None
    inputLine = 0
    scopeStep = 0
    scope = 0
    buffer = []
    stages = SparseList()

    def __init__( self, file ) -> None:
        self.input = open( file, 'r', encoding=ENCODING )
        self.inputLine = 0

        self.setStage( 0,   lex_rStrip )           # Clear any RHS whitespace, for a tiny speedup
        self.setStage( 10,  lex_blankBreaks )      # Handle blank lines
        self.setStage( 20,  lex_handleScope )      # Capture the scope depth
        self.setStage( 30,  lex_handleDirective )  # Search for a directive preamble, and short-form content...
        self.setStage( 100, lex_handleText )       # At this point, just assume the rest is text, and start emitting values

    def setStage( self, index: int, func ):
        if self.stages[index]:
            print( f"[WW]\tLexer stage {index} was already in use, but has been overwritten!" )
        self.stages[index] = func
    
    def clearStage( self, index:int, func ):
        if self.stages[index] and self.stages[index] != func:
            print( f"[WW]\tLexer stage {index} was in use, but not by the function supplied! Refusing to remove." )
            return
        self.stages[index] = None

    def nextToken(self) -> Token:
        
        # Attempt to fill the buffer
        while self.input.readable() and len(self.buffer) == 0:
            line = self.input.readline()
            self.inputLine += 1
            if not line:
                break
            
            for stage in self.stages:
                if stage:
                    line = stage( self, line )

        # Just dequeue if we already have buffered tokens
        if len(self.buffer) > 0:
            return self.buffer.pop(0)
        
        return None