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

import os
from importlib import import_module
from enum import auto
from Lexer import Lexer, TokenType, Token

SCRIPT_PATH = os.path.realpath( __file__ )

class Directive(auto):
    USE = "use"
    UNUSE = "unuse"
    TITLE = "title"
    FIGURE = "figure"

class Parser:
    libraries = {}
    lexer = None;
    nextToken = None;

    def __init__(self, lexer: Lexer) -> None:
        self.lexer = lexer
        self.nextToken = lexer.nextToken()
    
    def acceptToken( self, type: TokenType, value = None ):
        thisToken = self.nextToken

        # Blind accept! Avoid using this except for debug...
        if type == None:
            self.nextToken = self.lexer.nextToken()
            return thisToken;

        if self.nextToken:
            if self.nextToken.type == type:
                if value:
                    if self.nextToken.value == value:
                        self.nextToken = self.lexer.nextToken()
                        return thisToken
                    else:
                        raise Exception(f"Unexpected token. Wanted {type}/{value}, read {self.nextToken}")
                self.nextToken = self.lexer.nextToken()
                return thisToken
            raise Exception(f"Unexpected token. Wanted {type}/{value}, read {self.nextToken}")
        raise Exception(f"Reached the end of the token stream, but expected {type}/{value}")
    
    def parseDirective( self ):
        if self.nextToken.value == Directive.USE:
            return self.parseUse()
        
        if self.nextToken.value == Directive.UNUSE:
            return self.parseUnUse()
        
        if self.nextToken.value == Directive.TITLE:
            return self.parseTitle()

        if self.nextToken.value == Directive.FIGURE:
            raise Exception( "Unimplemented directive: FIGURE" )
        
        raise Exception( f"Unknown directive: {self.nextToken.value} on line {self.nextToken.line}. HALT" )

    def parseUse( self ):
        self.acceptToken( TokenType.DIRECTIVE, Directive.USE )
        library = self.acceptToken( TokenType.TEXT ).value
        addon = import_module( f"addons.{library}" )
        self.libraries[str(library)] = addon
        addon.bind( self )    
    
    def parseUnUse( self ):
        self.acceptToken( TokenType.DIRECTIVE, Directive.UNUSE )
        library = self.acceptToken( TokenType.TEXT ).value

        if library not in self.libraries:
            print( f"[WW]\tNo such library {library} loaded, skipped unbind." )
            return

        addon = self.libraries.pop(library); # Remove the library and keep a temporary reference...
        addon.unbind( self )
    
    def parseTitle( self ):
        directive = self.acceptToken( TokenType.DIRECTIVE, Directive.TITLE )

        args = {}
        while self.nextToken and self.nextToken.type == TokenType.ARGUMENT and self.nextToken.isChildOf( directive ):
            arg = self.parseArgument( directive )
            args[arg[0]] = arg[1]
        
        titleText = self.parseText( directive )

        print( f"New title: '{titleText.lstrip()}', args = {args}" )

    def parseArgument( self, parent ):
        argument = self.acceptToken( TokenType.ARGUMENT ).value
        value = self.parseText( parent )
        return [argument,value]

    def parseText( self, parent ):
        buffer = "";
        while self.nextToken and self.nextToken.type == TokenType.TEXT:
            buffer += ' ' + self.acceptToken( TokenType.TEXT ).value
        return buffer.lstrip()

    def parse( self ) -> list:
        currentScope = 0
        root = []
        while self.nextToken:
            if( self.nextToken.scope != currentScope and self.nextToken.type != TokenType.BREAK ):
                while( self.nextToken.scope != currentScope ):
                    if( self.nextToken.scope > currentScope ):
                        print( "<p>" );
                        currentScope += 1
                    elif( self.nextToken.scope < currentScope ):
                        print( "</p>" );
                        currentScope -= 1
                    
                currentScope = self.nextToken.scope

            if self.nextToken.type == TokenType.DIRECTIVE:
                self.parseDirective()
            
            elif self.nextToken.type == TokenType.TEXT:
                print( ('-' * self.nextToken.scope) + ' ' + self.acceptToken(TokenType.TEXT).value )
            
            elif self.nextToken.type == TokenType.BREAK:
                self.acceptToken( TokenType.BREAK )
                print( "BREAK" )

            else:
                print( f"Unknown token: {self.acceptToken( None )}" )
        
        return root