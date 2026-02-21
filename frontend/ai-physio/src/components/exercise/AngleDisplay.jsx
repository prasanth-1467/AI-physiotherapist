// Floating angle label at a joint's canvas position
export default function AngleDisplay({ angles = [], canvasWidth = 640, canvasHeight = 480 }) {
  // angles: [{ joint, value, inRange, x, y }]
  // x/y are normalized 0-1 from keypoints
  return (
    <div className="angle-display-layer" style={{ width: canvasWidth, height: canvasHeight }}>
      {angles.map((a, i) => (
        <div
          key={i}
          className={`angle-label ${a.inRange ? 'angle-in' : 'angle-out'}`}
          style={{
            left: `${(a.x || 0) * 100}%`,
            top: `${(a.y || 0) * 100}%`,
          }}
        >
          {a.joint}: {Math.round(a.value)}°
        </div>
      ))}
    </div>
  );
}
