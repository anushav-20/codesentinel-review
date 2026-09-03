# CodeSentinel - AI Code Review and Security Vulnerability Scanner

A static analysis tool that reviews Python source code for complexity issues and
security vulnerabilities, built entirely from scratch using Python's ast module
and pattern-based scanning rather than calling an external linter.

Tech Stack: Python, ast (built-in), Flask, React.js

## Features
- Cyclomatic complexity calculation per function using AST traversal
- Flags long functions, high argument counts, and deeply nested logic
- Security scanner catches hardcoded secrets, eval/exec usage, unsafe pickle
 deserialization, string-formatted SQL queries, and shell injection patterns
- Weighted overall risk score (0-100) combining complexity and security signals
- React interface to paste code and see issues flagged inline with line numbers

## How It Works
1. Source code is parsed into an abstract syntax tree using Python's ast module
2. `analyzers/complexity.py` walks each function node, counting decision points
 (if/for/while/try/except/boolean operators) to compute cyclomatic complexity
3. `analyzers/security.py` runs a set of regex rules against each line to catch
 common vulnerability patterns
4. Both signals are combined into a single risk score returned by the API

## Getting Started

### Backend
```
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python app.py
```
Server runs on http://localhost:5000

### Frontend
```
cd frontend
npm install
npm run dev
```
App runs on http://localhost:5173

## API
| Method | Endpoint | Description |
|--------|----------------|--------------------------------------------------|
| POST | /api/review | body: { "code": "..." } -- returns risk score, function-level complexity, and security findings |
| GET | /api/health | Health check |

## Roadmap
- Support for multi-file project scanning
- GitHub integration to review pull request diffs automatically
- Additional language support (JavaScript, Java)

---
Built by Anusha V - https://www.linkedin.com/in/anushav20
