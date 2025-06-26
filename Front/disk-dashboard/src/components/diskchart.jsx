import { Pie } from "react-chartjs-2";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";
ChartJS.register(ArcElement, Tooltip, Legend);

export default function DiskChart({ diskData }) {
  const data = {
    labels: ["Usado (GB)", "Libre (GB)"],
    datasets: [
      {
        data: [diskData.used_gb, diskData.free_gb],
        backgroundColor: ["#ef4444", "#10b981"],
        borderWidth: 1,
      },
    ],
  };

  return (
    <div className="max-w-xs mx-auto">
      <Pie data={data} />
    </div>
  );
}