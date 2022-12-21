#!/usr/bin/env python3

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

# Configure any global strings here, before we load anything
import os
CWD         = os.getcwd()
BUILD_PATH  = os.getenv("SDML_BUILD_PATH", os.path.join( CWD, "output" ) )
SOURCE_PATH = os.getenv("SDML_SOURCE_PATH", os.path.join( CWD ) )

from Logging import Log
from Lexer import Lexer, TokenType
from SDMLParser import Parser

def r_buildFileList( path, output=[] ):
    for f in os.listdir( path ):
        if os.path.isdir( os.path.join( path, f ) ):
            r_buildFileList( os.path.join( path, f ), output )
            continue

        if( f.lower().endswith('.sdml') ):
            output.append( os.path.join( path, f ) )
    return output


# Ensure we have somewhere to send stuff
if not os.path.exists( BUILD_PATH ):
    Log.info( "No build output path found, creating it" )
    os.mkdir( BUILD_PATH )

# Build a (flat) list of files to parse
fList = r_buildFileList( SOURCE_PATH )

# Work through the list :)
for f in fList:
    lex = Lexer( f )
    document = Parser( lex )

    output = document.parse()

    print( output )