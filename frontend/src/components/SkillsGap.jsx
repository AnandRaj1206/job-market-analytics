import { useState } from "react";
import { getSkillsGap } from "../api";

const CATEGORIES = ["Data Science", "Backend", "Frontend", "DevOps", "Product"];

export default function SkillsGap() {
  const [category, setCategory] = useState("Backend");
  const [skillsInput, setSkillsInput] = useState("Python, SQL, Docker");
  const [result, setResult] = useState(null);

  const handleCheck = async () => {
    const known = skillsInput.split(",").map((s) => s.trim()).filter(Boolean);
    const data = await getSkillsGap(category, known);
    setResult(data);
  };

  return (
    <div className="card">
      <div className="card-header">
        <h2 className="card-title">
          <span className="card-title-icon accent">🎯</span>
          Skills Gap Checker
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

        <input
          className="input-control"
          value={skillsInput}
          onChange={(e) => setSkillsInput(e.target.value)}
          placeholder="Your skills, comma-separated"
          style={{ flex: 1, minWidth: 200 }}
        />

        <button className="btn btn-accent" onClick={handleCheck}>
          Check Gap
        </button>
      </div>

      {result && (
        <div className="gap-results">
          <div>
            <div className="gap-section-title">Matching Skills You Possess</div>
            <div className="chips-container">
              {result.matching_skills && result.matching_skills.length > 0 ? (
                result.matching_skills.map((skill) => (
                  <span key={skill} className="chip chip-green">
                    ✓ {skill}
                  </span>
                ))
              ) : (
                <span style={{ fontSize: "0.85rem", color: "var(--text-muted)", fontStyle: "italic" }}>
                  None of the top skills for this role yet
                </span>
              )}
            </div>
          </div>

          <div>
            <div className="gap-section-title">Recommended Skills to Learn</div>
            <div className="chips-container">
              {result.missing_skills && result.missing_skills.length > 0 ? (
                result.missing_skills.map((skill) => (
                  <span key={skill} className="chip chip-indigo">
                    + {skill}
                  </span>
                ))
              ) : (
                <span style={{ fontSize: "0.85rem", color: "var(--text-muted)", fontStyle: "italic" }}>
                  Great job! You have all the top required skills.
                </span>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}