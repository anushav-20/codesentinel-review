"""
Static complexity analysis for Python source using the ast module.
Computes cyclomatic complexity per function and flags oversized functions —
the same signals real tools like radon/SonarQube surface, built from scratch.
"""
import ast


DECISION_NODES = (
    ast.If, ast.For, ast.While, ast.Try, ast.With,
    ast.BoolOp, ast.ExceptHandler,
)


def cyclomatic_complexity(func_node: ast.FunctionDef) -> int:
    complexity = 1
    for node in ast.walk(func_node):
        if isinstance(node, DECISION_NODES):
            complexity += 1
        if isinstance(node, ast.BoolOp):
            complexity += len(node.values) - 1
    return complexity


def analyze_functions(tree: ast.AST) -> list[dict]:
    results = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            body_lines = (node.end_lineno or node.lineno) - node.lineno + 1
            complexity = cyclomatic_complexity(node)
            num_args = len(node.args.args)

            issues = []
            if complexity > 10:
                issues.append(f"High cyclomatic complexity ({complexity}) — consider splitting this function")
            if body_lines > 50:
                issues.append(f"Long function ({body_lines} lines) — consider extracting helper functions")
            if num_args > 5:
                issues.append(f"Too many parameters ({num_args}) — consider a config object or dataclass")

            results.append({
                "name": node.name,
                "line": node.lineno,
                "complexity": complexity,
                "length_lines": body_lines,
                "num_args": num_args,
                "issues": issues,
            })
    return results
