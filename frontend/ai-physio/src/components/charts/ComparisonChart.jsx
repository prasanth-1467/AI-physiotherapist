import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
} from 'recharts';

export default function ComparisonChart({ data = [] }) {
  // data: [{ exercise: 'Knee Flex', day1: 55, day30: 82 }, ...]
  return (
    <div className="chart-wrapper">
      <ResponsiveContainer width="100%" height={260}>
        <BarChart data={data} margin={{ top: 10, right: 20, left: 0, bottom: 20 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
          <XAxis dataKey="exercise" tick={{ fontSize: 11 }} angle={-15} textAnchor="end" />
          <YAxis domain={[0, 100]} tick={{ fontSize: 12 }} />
          <Tooltip />
          <Legend />
          <Bar dataKey="day1" name="Day 1" fill="#90a4ae" radius={[4, 4, 0, 0]} />
          <Bar dataKey="day30" name="Day 30" fill="#4caf50" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
