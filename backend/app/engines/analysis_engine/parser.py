import ast
from pathlib import Path

class PythonParser:
    def parse_file(self, file_path: Path):
        source_code = file_path.read_text(encoding="utf-8")
        tree = ast.parse(source_code)

        return {
            "functions": self.extract_functions(tree, source_code),
            "classes": self.extract_classes(tree, source_code),
            "imports": self.extract_imports(tree)
        }


    def extract_functions(self, tree, source_code):
        functions = []

        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                functions.append({
                    "name": node.name,
                    "arguments": [arg.arg for arg in node.args.args],
                    "docstring": ast.get_docstring(node),
                    "source": ast.get_source_segment(source_code, node)
                    })

        return functions

    def extract_classes(self, tree, source_code):
        classes = []

        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                methods = []

                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        methods.append(item.name)

                classes.append({
                    "name": node.name,
                    "docstring": ast.get_docstring(node),
                    "methods": methods,
                    "source": ast.get_source_segment(source_code, node)
                })

        return classes

    def extract_imports(self, tree):
        imports = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                     imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module if node.module else ""

                for alias in node.names:
                    if module:
                        imports.append(f"{module}.{alias.name}")
                    else:
                        imports.append(alias.name)

        return imports


