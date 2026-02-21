import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Cell, ResponsiveContainer,
} from 'recharts';

export default function JointBarChart({ data = [] }) {
  // data: [{ joint: 'Knee', improvement: 15 }, ...]
  return (
    <div className="chart-wrapper">
      <ResponsiveContainer width="100%" height={Math.max(200, data.length * 40)}>
        <BarChart
          layout="vertical"
          data={data}
          margin={{ top: 5, right: 30, left: 60, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
          <XAxis type="number" domain={['dataMin', 'dataMax']} tick={{ fontSize: 12 }} unit="%" />
          <YAxis type="category" dataKey="joint" tick={{ fontSize: 12 }} width={60} />
          <Tooltip formatter={v => [`${v}%`, 'Improvement']} />
          <Bar dataKey="improvement" radius={[0, 4, 4, 0]}>
            {data.map((entry, i) => (
              <Cell key={i} fill={entry.improvement >= 0 ? '#4caf50' : '#f44336'} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
