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
""" Delete the staticmethod decorator from __new__ methods if provided.

CPython made these optional, and applies them to every __new__. We better add
them early, so our analysis will see it for improved consistency. This is better
then adding it during code generation only.
"""

from .OptimizeBase import OptimizationVisitorBase

from nuitka import Nodes

class FixupNewStaticMethodVisitor( OptimizationVisitorBase ):
    def __call__( self, node ):
        if node.isStatementFunctionBuilder() and \
           node.getFunctionName() == "__new__" and \
           node.getParentClass() is not None:

            decorators = node.getDecorators()

            if len( decorators ) == 0:
                new_node = Nodes.CPythonExpressionVariableRef(
                    variable_name = "staticmethod",
                    source_ref    = node.getSourceReference()
                )

                node.setDecorators(
                    ( new_node, )
                )
                new_node.parent = node

                self.signalChange(
                    "new_code",
                    node.getSourceReference(),
                    "Added missing staticmethod decoration to __new__ method"
                )