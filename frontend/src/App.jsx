import React, { useState } from "react";
import axios from "axios";

const API = "http://localhost:5000/api";
const SAMPLE = `def process_login(username, password):
    query = "SELECT * FROM users WHERE name='%s'" % username
    api_key = "sk_live_abc123456789"
    if eval(password) == "admin":
        return True
`;

export default function App() {
  const [code, setCode] = useState(SAMPLE);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const runReview = async () => {
    setLoading(true);
    try {
      const res = await axios.post(`${API}/review`, { code });
      setResult(res.data);
    } finally {
      setLoading(false);
    }
  };

  const sevColor = { critical: "#ef4444", high: "#f97316", low: "#eab308" };

  return (
    <div className="app">
      <header>
        <h1>CodeSentinel</h1>
        <p>Static code review: complexity analysis + security scanning</p>
      </header>

      <textarea value={code} onChange={(e) => setCode(e.target.value)} rows={14} />
      <button onClick={runReview} disabled={loading}>{loading ? "Analyzing..." : "Run Review"}</button>

      {result && (
        <div className="results">
          <div className="score-card">
            <span className="score">{result.risk_score}/100</span>
            <p>{result.verdict}</p>
          </div>

          <h3>Functions</h3>
          {result.functions.map((f) => (
            <div key={f.name} className="func-card">
              <strong>{f.name}()</strong> — line {f.line}, complexity {f.complexity}, {f.length_lines} lines
              {f.issues.map((i) => <p key={i} className="issue">{i}</p>)}
            </div>
          ))}

          <h3>Security Findings</h3>
          {result.security_findings.length === 0 && <p className="clean">No security issues detected.</p>}
          {result.security_findings.map((s, idx) => (
            <div key={idx} className="finding" style={{ borderLeftColor: sevColor[s.severity] }}>
              <span className="severity" style={{ color: sevColor[s.severity] }}>{s.severity.toUpperCase()}</span>
              <p>{s.message}</p>
              <code>line {s.line}: {s.snippet}</code>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
