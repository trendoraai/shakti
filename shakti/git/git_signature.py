import ast
import astor
import argparse
import os
from shakti.utils import register_help
from shakti.git.utils import is_ignored, get_ignore_patterns  # Add this import


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
def git_signature(paths, retain_docstring=False, retain_full_docstring=False):
    """Extract function and class signatures from Python files and folders.

    Usage: s git signature [--retain-docstring] [--retain-full-docstring] <path1> <path2> ...

    Paths can be individual Python files or folders containing Python files.
    Non-Python files will be skipped.
    Files and folders specified in .gitdiffignore will be ignored.
    """
    # Get ignore patterns
    ignore_patterns = get_ignore_patterns()

    def process_file(file_path):
        # Check if the file should be ignored
        if is_ignored(file_path, ignore_patterns):
            print(f"Skipping {file_path}: Ignored by .gitdiffignore")
            return

        _, ext = os.path.splitext(file_path)
        if ext.lower() != ".py":
            print(
                f"Skipping {file_path}: Only Python (.py) files are currently supported."
            )
            return

        try:
            with open(file_path, "r") as file:
                source_code = file.read()
            print("=" * 100)
            print(f"Signature for file: {file_path}")
            tree = ast.parse(source_code)
            extractor = SignatureExtractor(retain_docstring, retain_full_docstring)
            extractor.visit(tree)
            transformed_code = astor.to_source(extractor.new_tree)
            print(transformed_code)
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    for path in paths:
        if os.path.isfile(path):
            process_file(path)
        elif os.path.isdir(path):
            for root, _, files in os.walk(path):
                for file in files:
                    if file.endswith(".py"):
                        file_path = os.path.join(root, file)
                        process_file(file_path)
        else:
            print(f"Error: {path} is not a valid file or directory.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract function and class signatures from Python files and folders."
    )
    parser.add_argument(
        "paths",
        metavar="PATH",
        type=str,
        nargs="+",
        help="Python files or folders to analyze",
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

    git_signature(args.paths, args.retain_docstring, args.retain_full_docstring)
