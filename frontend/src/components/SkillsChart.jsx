import { useEffect, useState } from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import { getTopSkills } from "../api";

export default function SkillsChart() {
  const [data, setData] = useState([]);

  useEffect(() => {
    getTopSkills().then(setData);
  }, []);

  return (
    <div className="card">
      <div className="card-header">
        <h2 className="card-title">
          <span className="card-title-icon">📊</span>
          Top In-Demand Skills
        </h2>
      </div>
      <div style={{ width: "100%", height: 320 }}>
        <ResponsiveContainer>
          <BarChart data={data} layout="vertical" margin={{ top: 5, right: 20, left: 40, bottom: 5 }}>
            <XAxis type="number" stroke="#94a3b8" fontSize={12} tickLine={false} />
            <YAxis dataKey="skill" type="category" stroke="#64748b" fontSize={13} tickLine={false} axisLine={false} />
            <Tooltip
              contentStyle={{
                backgroundColor: "#0f172a",
                borderColor: "#334155",
                borderRadius: "8px",
                color: "#ffffff",
                fontSize: "13px",
                boxShadow: "0 10px 15px -3px rgba(0,0,0,0.3)"
              }}
              itemStyle={{ color: "#818cf8" }}
              cursor={{ fill: "rgba(79, 70, 229, 0.06)" }}
            />
            <Bar dataKey="count" fill="#4f46e5" radius={[0, 6, 6, 0]} barSize={20} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
