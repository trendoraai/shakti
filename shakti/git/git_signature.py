import ast
import astor
import argparse
from shakti.utils import register_help


class SignatureExtractor(ast.NodeVisitor):
    """Extract function and class signatures from Python files."""

    def __init__(self, retain_docstring, retain_full_docstring):
        self.retain_docstring = retain_docstring
        self.retain_full_docstring = retain_full_docstring
        self.new_tree = ast.Module(body=[], type_ignores=[])

    def visit_Import(self, node):
        self.new_tree.body.append(node)

    def visit_ImportFrom(self, node):
        self.new_tree.body.append(node)

    def extract_docstring(self, node):
        if (
            node.body
            and isinstance(node.body[0], ast.Expr)
            and isinstance(node.body[0].value, ast.Constant)
        ):
            docstring = node.body[0].value.value.strip()
            if self.retain_full_docstring:
                return ast.Expr(value=ast.Constant(value=docstring))
            elif self.retain_docstring:
                first_line = docstring.split("\n")[0]
                return ast.Expr(value=ast.Constant(value=first_line))
        return None

    def visit_FunctionDef(self, node):
        new_node = ast.FunctionDef(
            name=node.name,
            args=node.args,
            body=[],
            decorator_list=node.decorator_list,
            returns=node.returns,
        )
        docstring = self.extract_docstring(node)
        if docstring:
            new_node.body.append(docstring)
        new_node.body.append(
            ast.Expr(
                value=ast.Constant(
                    value="Function body here (ommitted for abbreviation), if needed ask for it."
                )
            )
        )
        self.new_tree.body.append(new_node)

    def visit_AsyncFunctionDef(self, node):
        new_node = ast.AsyncFunctionDef(
            name=node.name,
            args=node.args,
            body=[],
            decorator_list=node.decorator_list,
            returns=node.returns,
        )
        docstring = self.extract_docstring(node)
        if docstring:
            new_node.body.append(docstring)
        new_node.body.append(
            ast.Expr(
                value=ast.Constant(
                    value="Function body here (ommitted for abbreviation), if needed ask for it."
                )
            )
        )
        self.new_tree.body.append(new_node)

    def visit_ClassDef(self, node):
        new_node = ast.ClassDef(
            name=node.name,
            bases=node.bases,
            keywords=node.keywords,
            body=[],
            decorator_list=node.decorator_list,
        )
        docstring = self.extract_docstring(node)
        if docstring:
            new_node.body.append(docstring)
        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self.visit(item)
                new_node.body.append(self.new_tree.body.pop())
        self.new_tree.body.append(new_node)


@register_help("git signature")
def git_signature(source_code, retain_docstring, retain_full_docstring):
    """Extract function and class signatures from Python files.

    Usage: s git signature [--retain-docstring] [--retain-full-docstring] <file1> <file2> ...

    Note: Currently only supports Python (.py) files. Other file types will be skipped.
    """
    tree = ast.parse(source_code)
    extractor = SignatureExtractor(retain_docstring, retain_full_docstring)
    extractor.visit(tree)
    return astor.to_source(extractor.new_tree)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract function and class signatures from Python files."
    )
    parser.add_argument(
        "files", metavar="F", type=str, nargs="+", help="Python files to analyze"
    )
    parser.add_argument(
        "--retain-docstring",
        action="store_true",
        help="Retain docstrings",
    )
    parser.add_argument(
        "--retain-full-docstring",
        action="store_true",
        help="Retain full docstrings (overrides --retain-docstring)",
    )
    args = parser.parse_args()

    for file_path in args.files:
        with open(file_path, "r") as file:
            source_code = file.read()
        print(f"Extracting signatures from {file_path}:")
        try:
            transformed_code = git_signature(
                source_code, args.retain_docstring, args.retain_full_docstring
            )
            print(transformed_code)
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
