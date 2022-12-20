#!/usr/bin/env python3

# Configure any global strings here, before we load anything
import os
CWD         = os.getcwd()
BUILD_PATH  = os.getenv("SDML_BUILD_PATH", os.path.join( CWD, "output" ) )
SOURCE_PATH = os.getenv("SDML_SOURCE_PATH", os.path.join( CWD ) )

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


# Build a (flat) list of files to parse
fList = r_buildFileList( SOURCE_PATH )

# Work through the list :)
for f in fList:
    lex = Lexer( f )
    document = Parser( lex )

    output = document.parse()

    print( output )