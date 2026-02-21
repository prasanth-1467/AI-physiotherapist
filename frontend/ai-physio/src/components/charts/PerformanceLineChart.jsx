import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
} from 'recharts';

export default function PerformanceLineChart({ data = [] }) {
  // data: [{ day: 'Mon', score: 78 }, ...]
  return (
    <div className="chart-wrapper">
      <ResponsiveContainer width="100%" height={220}>
        <LineChart data={data} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
          <XAxis dataKey="day" tick={{ fontSize: 12 }} />
          <YAxis domain={[0, 100]} tick={{ fontSize: 12 }} />
          <Tooltip formatter={v => [`${v}`, 'Score']} />
          <Line
            type="monotone"
            dataKey="score"
            stroke="#4caf50"
            strokeWidth={2.5}
            dot={{ r: 4, fill: '#4caf50' }}
            activeDot={{ r: 6 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
