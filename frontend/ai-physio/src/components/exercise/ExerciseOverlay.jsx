import { useEffect, useRef } from 'react';

// MediaPipe BlazePose connections (landmark index pairs)
const CONNECTIONS = [
  [11, 12], [11, 13], [13, 15], [12, 14], [14, 16],
  [11, 23], [12, 24], [23, 24], [23, 25], [24, 26],
  [25, 27], [26, 28], [27, 29], [28, 30], [29, 31], [30, 32],
];

export default function ExerciseOverlay({ canvasRef, keypoints = [], angles = [] }) {
  // angles: [{ joint, value, inRange }]
  useEffect(() => {
    const canvas = canvasRef?.current;
    if (!canvas || !keypoints.length) return;
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    const W = canvas.width;
    const H = canvas.height;

    // Build index → point map
    const pts = {};
    keypoints.forEach((kp, i) => {
      if (kp && kp.visibility > 0.4) {
        pts[i] = { x: kp.x * W, y: kp.y * H };
      }
    });

    // Build joint → inRange lookup from angles
    const rangeMap = {};
    angles.forEach(a => { rangeMap[a.joint] = a.inRange; });

    // Draw bones
    CONNECTIONS.forEach(([a, b]) => {
      if (pts[a] && pts[b]) {
        ctx.beginPath();
        ctx.moveTo(pts[a].x, pts[a].y);
        ctx.lineTo(pts[b].x, pts[b].y);
        ctx.strokeStyle = '#00e676';
        ctx.lineWidth = 2;
        ctx.stroke();
      }
    });

    // Draw joints
    Object.values(pts).forEach(pt => {
      ctx.beginPath();
      ctx.arc(pt.x, pt.y, 5, 0, 2 * Math.PI);
      ctx.fillStyle = '#ffffff';
      ctx.fill();
      ctx.strokeStyle = '#00e676';
      ctx.lineWidth = 2;
      ctx.stroke();
    });
  }, [keypoints, angles, canvasRef]);

  return null; // canvas is managed by parent
}
