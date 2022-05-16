import sys
import ast
import importlib
import importlib.abc
import importlib.util


# Reads AST, find floats and auto round them 
# https://docs.python.org/3/library/ast.html
def auto_round(code):

    class TreeEditor(ast.NodeTransformer):
        def visit_Constant(self, node):
            return ast.Call(
                func=ast.Name(id='round', ctx=ast.Load()),
                args=[ast.Constant(value=node.value), ast.Constant(value=2)],
                keywords=[]
            )
        
    tree_editor = TreeEditor()
    
    code_ast = ast.parse(code)
    edited_code_ast = tree_editor.visit(code_ast)
    return ast.unparse(edited_code_ast) # ast.unparse only available in Python 3.9 and up


# Import hook that call's the AST manipulation function, auto_round
class ImportRewrite(importlib.abc.MetaPathFinder, importlib.abc.Loader):

    def find_spec(self, fullname, path=None, target=None):
        self.spec = importlib.machinery.PathFinder.find_spec(fullname, path)
        return importlib.util.spec_from_file_location(
            name=fullname, 
            location=self.spec.origin, 
            loader=self, 
            submodule_search_locations=self.spec.submodule_search_locations
        )

    def create_module(self, spec):
        return None

    def exec_module(self, module):
        with open(module.__spec__.origin,'r') as f:
            code = f.read()
        edited_code = auto_round(code)
        exec(edited_code, module.__dict__)


# Set a new import hook 
sys.meta_path.insert(0, ImportRewrite())













# ---------------------#
#     Original Code    |
#----------------------#


import myassert

myassert.test_equal()
