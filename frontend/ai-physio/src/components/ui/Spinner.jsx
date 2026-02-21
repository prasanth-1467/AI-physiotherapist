export default function Spinner({ size = 32, color = '#4caf50' }) {
  return (
    <div
      className="spinner"
      style={{
        width: size,
        height: size,
        borderColor: `${color}33`,
        borderTopColor: color,
      }}
    />
  );
}
