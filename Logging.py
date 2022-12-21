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

from os import getenv
from enum import IntEnum

colour = getenv( "SDML_COLOR_LOGS", "TRUE" ) == "TRUE"
try:
    from colorama import Fore, Back, Style
except ImportError as e:
    colour = False
    pass

class LogLevel(IntEnum):
    DEBUG = 3
    INFO = 2
    WARNING = 1
    ERROR = 0

class Log:
    prefix = False
    level = LogLevel.WARNING

    @staticmethod
    def __fmtLogStr( type, text ) -> str:
        return f"[{type}]  {text}"
    
    @staticmethod
    def __styleLogStr( style, type, text ) -> str:
        return f"{style}{Log.__fmtLogStr( type, text )}{Style.RESET_ALL}"

    @staticmethod
    def debug( text ):
        if Log.level < LogLevel.DEBUG:
            return
        
        if( colour ):
            print( Log.__styleLogStr( Fore.CYAN, '  ', text ) )
        else:
            print( Log.__fmtLogStr( '  ', text ) )

    @staticmethod
    def info( text ):
        if Log.level < LogLevel.INFO:
            return
        
        if( colour ):
            print( Log.__styleLogStr( Fore.WHITE, 'II', text ) )
        else:
            print( Log.__fmtLogStr( 'II', text ) )

    @staticmethod
    def warn( text ):
        if Log.level < LogLevel.WARNING:
            return
        
        if( colour ):
            print( Log.__styleLogStr( Style.BRIGHT + Fore.YELLOW, 'WW', text ) )
        else:
            print( Log.__fmtLogStr( 'WW', text ) )

    @staticmethod
    def error( text ):
        if Log.level < LogLevel.ERROR:
            return
        
        if( colour ):
            print( Log.__styleLogStr( Style.BRIGHT + Fore.RED, 'EE', text ) )
        else:
            print( Log.__fmtLogStr( 'EE', text ) )