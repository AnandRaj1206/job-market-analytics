import { useState } from "react";
import { generateReport, getReportDownloadUrl } from "../api";

const CATEGORIES = ["Data Science", "Backend", "Frontend", "DevOps", "Product"];

export default function CareerReport() {
  const [category, setCategory] = useState("Data Science");
  const [report, setReport] = useState("");
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    setLoading(true);
    setReport("");
    try {
      const md = await generateReport(category);
      setReport(md);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <div className="card-header">
        <h2 className="card-title">
          <span className="card-title-icon">📄</span>
          Career Report Generator
        </h2>
      </div>

      <div className="form-row">
        <select
          className="select-control"
          value={category}
          onChange={(e) => setCategory(e.target.value)}
        >
          {CATEGORIES.map((c) => (
            <option key={c} value={c}>{c}</option>
          ))}
        </select>

        <button className="btn btn-primary" onClick={handleGenerate} disabled={loading}>
          {loading ? "Generating..." : "Generate Report"}
        </button>

        {report && (
          <a
            className="btn btn-outline"
            href={getReportDownloadUrl(category)}
            target="_blank"
            rel="noreferrer"
          >
            📥 Download .md
          </a>
        )}
      </div>

      {report ? (
        <pre className="report-preview">
          {report}
        </pre>
      ) : null}
    </div>
  );
}