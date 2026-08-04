import { useEffect, useState } from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import { getTopLocations } from "../api";

export default function LocationsChart() {
  const [data, setData] = useState([]);

  useEffect(() => {
    getTopLocations().then(setData);
  }, []);

  return (
    <div className="card">
      <div className="card-header">
        <h2 className="card-title">
          <span className="card-title-icon accent">📍</span>
          Top Hiring Locations
        </h2>
      </div>
      <div style={{ width: "100%", height: 300 }}>
        <ResponsiveContainer>
          <BarChart data={data} layout="vertical" margin={{ top: 5, right: 20, left: 60, bottom: 5 }}>
            <XAxis type="number" stroke="#94a3b8" fontSize={12} tickLine={false} />
            <YAxis dataKey="location" type="category" stroke="#64748b" fontSize={13} tickLine={false} axisLine={false} width={90} />
            <Tooltip
              contentStyle={{
                backgroundColor: "#0f172a",
                borderColor: "#334155",
                borderRadius: "8px",
                color: "#ffffff",
                fontSize: "13px",
                boxShadow: "0 10px 15px -3px rgba(0,0,0,0.3)"
              }}
              itemStyle={{ color: "#34d399" }}
              cursor={{ fill: "rgba(16, 185, 129, 0.06)" }}
            />
            <Bar dataKey="count" fill="#10b981" radius={[0, 6, 6, 0]} barSize={20} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}