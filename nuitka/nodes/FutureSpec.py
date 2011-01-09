#
#     Copyright 2011, Kay Hayen, mailto:kayhayen@gmx.de
#
#     Part of "Nuitka", an optimizing Python compiler that is compatible and
#     integrates with CPython, but also works on its own.
#
#     If you submit Kay Hayen patches to this software in either form, you
#     automatically grant him a copyright assignment to the code, or in the
#     alternative a BSD license to the code, should your jurisdiction prevent
#     this. Obviously it won't affect code that comes to him indirectly or
#     code you don't submit to him.
#
#     This is to reserve my ability to re-license the code at any time, e.g.
#     the PSF. With this version of Nuitka, using it for Closed Source will
#     not be allowed.
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, version 3 of the License.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#     Please leave the whole of this copyright notice intact.
#
""" Specification record for future flags.

A source reference also implies a specific set of future flags in use by the parser at
that location. Can be different inside a module due to e.g. the inlining of exec
statements with their own future imports, or inlining of code from other modules.
"""

from nuitka.Utils import getPythonVersion

class FutureSpec:
    def __init__( self ):
        self._future_division   = getPythonVersion() >= 300
        self._unicode_literals  = getPythonVersion() >= 300
        self._absolute_import   = getPythonVersion() >= 270
        self._future_print      = getPythonVersion() >= 300

    def clone( self ):
        result = FutureSpec()

        result._future_division   = self._unicode_literals
        result._unicode_literals  = self._unicode_literals
        result._absolute_import   = self._absolute_import
        result._future_print      = self._future_print

        return result

    def isFutureDivision( self ):
        return self._future_division

    def enableFutureDivision( self ):
        self._future_division = True

    def enableFuturePrint( self ):
        self._future_print = True

    def enableUnicodeLiterals( self ):
        self._unicode_literals = True

    def enableAbsoluteImport( self ):
        self._absolute_import = True

    def asFlags( self ):
        result = []

        if self._future_division:
            result.append( "CO_FUTURE_DIVISION" )

        if self._unicode_literals:
            result.append( "CO_FUTURE_UNICODE_LITERALS" )

        if self._absolute_import:
            result.append( "CO_FUTURE_ABSOLUTE_IMPORT" )

        if self._future_print:
            result.append( "CO_FUTURE_PRINT_FUNCTION" )

        return result