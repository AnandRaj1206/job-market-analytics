import axios from "axios";

const api = axios.create({ baseURL: "https://job-market-analytics-e5hu.onrender.com" });

export const getTopSkills = () => api.get("/analytics/top-skills").then(r => r.data);
export const getSalaryTrends = () => api.get("/analytics/salary-trends").then(r => r.data);
export const getTopLocations = () => api.get("/analytics/top-locations").then(r => r.data);
export const sendChatMessage = (message) => api.post("/chat/", { message }).then(r => r.data.reply);
export const getSkillsGap = (category, knownSkills) =>
  api.post("/analytics/skills-gap", { category, known_skills: knownSkills }).then(r => r.data);
export const generateReport = (category) =>
  api.post("/chat/report", { category }).then(r => r.data.report_markdown);
export const getReportDownloadUrl = (category) =>
  `http://localhost:8000/api/chat/report/download?category=${encodeURIComponent(category)}`;

export default api;