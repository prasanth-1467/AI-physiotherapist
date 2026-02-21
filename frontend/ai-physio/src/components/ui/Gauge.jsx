// Semicircular arc gauge showing current angle vs ideal range
export default function Gauge({ minAngle = 0, maxAngle = 180, idealMin = 60, idealMax = 120, currentAngle = null }) {
  const cx = 100, cy = 100, r = 80;
  const toRad = (deg) => (deg / 180) * Math.PI;

  function polarToXY(angleDeg) {
    // 0deg = left, 180deg = right (semicircle opening downward)
    const rad = Math.PI - toRad(angleDeg);
    return {
      x: cx + r * Math.cos(rad),
      y: cy - r * Math.sin(rad),
    };
  }

  function arcPath(startDeg, endDeg, color) {
    const start = polarToXY(startDeg);
    const end = polarToXY(endDeg);
    const largeArc = endDeg - startDeg > 180 ? 1 : 0;
    return (
      <path
        d={`M ${start.x} ${start.y} A ${r} ${r} 0 ${largeArc} 0 ${end.x} ${end.y}`}
        stroke={color}
        strokeWidth="12"
        fill="none"
        strokeLinecap="round"
      />
    );
  }

  const needlePos = currentAngle !== null ? polarToXY(Math.min(maxAngle, Math.max(minAngle, currentAngle))) : null;
  const inRange = currentAngle !== null && currentAngle >= idealMin && currentAngle <= idealMax;

  return (
    <div className="gauge-wrapper">
      <svg viewBox="0 0 200 110" width="200" height="110">
        {/* Background arc */}
        {arcPath(minAngle, maxAngle, '#e0e0e0')}
        {/* Ideal range arc */}
        {arcPath(idealMin, idealMax, '#4caf50')}
        {/* Needle */}
        {needlePos && (
          <>
            <line
              x1={cx} y1={cy}
              x2={needlePos.x} y2={needlePos.y}
              stroke={inRange ? '#2196f3' : '#f44336'}
              strokeWidth="3"
              strokeLinecap="round"
            />
            <circle cx={cx} cy={cy} r="5" fill="#555" />
          </>
        )}
      </svg>
      {currentAngle !== null && (
        <div className={`gauge-label ${inRange ? 'gauge-in' : 'gauge-out'}`}>
          {currentAngle}°
        </div>
      )}
    </div>
  );
}
