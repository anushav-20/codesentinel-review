"""
CodeSentinel - AI Code Review & Security Vulnerability Scanner

Accepts a Python source file or pasted snippet, runs it through:
1. AST-based complexity analysis (cyclomatic complexity, function length, arg count)
2. Pattern-based security scanning (hardcoded secrets, eval/exec, unsafe pickle, SQL injection)
3. A weighted overall risk score combining both signals

No external LLM calls are used -- this is a from-scratch static analysis engine.
"""
import ast
from flask import Flask, request, jsonify
from flask_cors import CORS

from analyzers.complexity import analyze_functions
from analyzers.security import scan_security

app = Flask(__name__)
CORS(app)

SEVERITY_WEIGHTS = {"critical": 25, "high": 15, "low": 5}


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/api/review", methods=["POST"])
def review():
    data = request.get_json()
    source = data.get("code", "")
    if not source.strip():
        return jsonify({"error": "No code provided"}), 400

    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        return jsonify({"error": f"Syntax error: {e}"}), 400

    functions = analyze_functions(tree)
    security_findings = scan_security(source)

    complexity_penalty = sum(min(f["complexity"], 20) for f in functions)
    security_penalty = sum(SEVERITY_WEIGHTS.get(f["severity"], 5) for f in security_findings)

    risk_score = max(0, 100 - complexity_penalty - security_penalty)

    if risk_score >= 80:
        verdict = "Low risk -- code looks clean"
    elif risk_score >= 50:
        verdict = "Moderate risk -- some issues worth addressing"
    else:
        verdict = "High risk -- review flagged issues before merging"

    return jsonify({
        "risk_score": risk_score,
        "verdict": verdict,
        "functions": functions,
        "security_findings": security_findings,
        "summary": {
            "total_functions": len(functions),
            "flagged_functions": sum(1 for f in functions if f["issues"]),
            "security_issues": len(security_findings),
        },
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)
