"""
Lightweight security scanner for Python source using pattern matching —
catches common vulnerability classes: hardcoded secrets, dangerous eval/exec
usage, unsafe deserialization, and string-formatted SQL queries.
"""
import re

SECURITY_PATTERNS = [
    {
        "id": "hardcoded-secret",
        "pattern": re.compile(r'(password|api_key|secret|token)\s*=\s*["\'][^"\']{4,}["\']', re.IGNORECASE),
        "severity": "high",
        "message": "Possible hardcoded credential. Use environment variables or a secrets manager instead.",
    },
    {
        "id": "eval-usage",
        "pattern": re.compile(r'\beval\s*\('),
        "severity": "critical",
        "message": "Use of eval() can execute arbitrary code — avoid or sanitize input strictly.",
    },
    {
        "id": "exec-usage",
        "pattern": re.compile(r'\bexec\s*\('),
        "severity": "critical",
        "message": "Use of exec() can execute arbitrary code — avoid or sanitize input strictly.",
    },
    {
        "id": "unsafe-pickle",
        "pattern": re.compile(r'pickle\.loads?\s*\('),
        "severity": "high",
        "message": "Deserializing untrusted data with pickle can lead to remote code execution.",
    },
    {
        "id": "sql-string-format",
        "pattern": re.compile(r'(execute|cursor\.execute)\s*\(\s*["\'].*%s.*["\']\s*%'),
        "severity": "high",
        "message": "String-formatted SQL query detected — use parameterized queries to prevent SQL injection.",
    },
    {
        "id": "shell-injection",
        "pattern": re.compile(r'(os\.system|subprocess\.(call|run|Popen))\s*\([^)]*\+'),
        "severity": "high",
        "message": "Shell command built via string concatenation — risk of command injection.",
    },
    {
        "id": "debug-mode",
        "pattern": re.compile(r'debug\s*=\s*True', re.IGNORECASE),
        "severity": "low",
        "message": "Debug mode enabled — should be disabled in production.",
    },
]


def scan_security(source: str) -> list[dict]:
    findings = []
    lines = source.splitlines()
    for lineno, line in enumerate(lines, start=1):
        for rule in SECURITY_PATTERNS:
            if rule["pattern"].search(line):
                findings.append({
                    "rule_id": rule["id"],
                    "severity": rule["severity"],
                    "line": lineno,
                    "message": rule["message"],
                    "snippet": line.strip()[:120],
                })
    return findings
