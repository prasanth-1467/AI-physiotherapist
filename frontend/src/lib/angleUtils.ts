export type Point = { x: number; y: number; z?: number; visibility?: number };

export const calculateAngle = (a: Point, b: Point, c: Point): number => {
    const radians = Math.atan2(c.y - b.y, c.x - b.x) - Math.atan2(a.y - b.y, a.x - b.x);
    let angle = Math.abs((radians * 180.0) / Math.PI);

    if (angle > 180.0) {
        angle = 360 - angle;
    }

    return Math.round(angle);
};

export const getJointAngles = (landmarks: Point[]) => {
    if (!landmarks || landmarks.length === 0) return null;

    return {
        left_elbow: calculateAngle(landmarks[11], landmarks[13], landmarks[15]),
        right_elbow: calculateAngle(landmarks[12], landmarks[14], landmarks[16]),
        left_shoulder: calculateAngle(landmarks[13], landmarks[11], landmarks[23]),
        right_shoulder: calculateAngle(landmarks[14], landmarks[12], landmarks[24]),
        left_knee: calculateAngle(landmarks[23], landmarks[25], landmarks[27]),
        right_knee: calculateAngle(landmarks[24], landmarks[26], landmarks[28]),
        left_hip: calculateAngle(landmarks[11], landmarks[23], landmarks[25]),
        right_hip: calculateAngle(landmarks[12], landmarks[24], landmarks[26]),
    };
};
