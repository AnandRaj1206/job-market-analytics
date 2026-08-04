import SkillsChart from "./SkillsChart";
import LocationsChart from "./LocationsChart";
import ChatWidget from "./ChatWidget";
import CareerReport from "./CareerReport";
import SkillsGap from "./SkillsGap";

export default function Dashboard() {
  return (
    <div>
      <div className="dashboard-grid-top">
        <div className="dashboard-charts-column">
          <SkillsChart />
          <LocationsChart />
        </div>
        <ChatWidget />
      </div>
      <div className="dashboard-grid-bottom">
        <CareerReport />
        <SkillsGap />
      </div>
    </div>
  );
}