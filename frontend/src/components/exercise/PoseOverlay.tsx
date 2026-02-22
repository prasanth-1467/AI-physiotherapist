'use client';

import React, { useRef, useEffect } from 'react';
import { PoseLandmarkerResult } from '@mediapipe/tasks-vision';

interface PoseOverlayProps {
    results: PoseLandmarkerResult | null;
    width: number;
    height: number;
}

export const PoseOverlay: React.FC<PoseOverlayProps> = ({ results, width, height }) => {
    const canvasRef = useRef<HTMLCanvasElement>(null);

    useEffect(() => {
        if (!canvasRef.current || !results || !results.landmarks || results.landmarks.length === 0) return;

        const ctx = canvasRef.current.getContext('2d');
        if (!ctx) return;

        ctx.clearRect(0, 0, width, height);

        const landmarks = results.landmarks[0];

        // Draw Connections
        ctx.strokeStyle = '#2BBFBF';
        ctx.lineWidth = 4;
        ctx.lineCap = 'round';

        const connections = [
            [11, 12], [11, 13], [13, 15], [12, 14], [14, 16], // Shoulders and arms
            [11, 23], [12, 24], [23, 24], // Torso
            [23, 25], [25, 27], [24, 26], [26, 28] // Legs
        ];

        connections.forEach(([i, j]) => {
            const p1 = landmarks[i];
            const p2 = landmarks[j];
            if (p1 && p2 && (p1.visibility ?? 1) > 0.5 && (p2.visibility ?? 1) > 0.5) {
                ctx.beginPath();
                ctx.moveTo(p1.x * width, p1.y * height);
                ctx.lineTo(p2.x * width, p2.y * height);
                ctx.stroke();
            }
        });

        // Draw Landmarks
        landmarks.forEach((landmark) => {
            if ((landmark.visibility ?? 1) > 0.5) {
                ctx.fillStyle = '#FFFFFF';
                ctx.strokeStyle = '#2BBFBF';
                ctx.lineWidth = 2;
                ctx.beginPath();
                ctx.arc(landmark.x * width, landmark.y * height, 5, 0, 2 * Math.PI);
                ctx.fill();
                ctx.stroke();
            }
        });
    }, [results, width, height]);

    return (
        <canvas
            ref={canvasRef}
            width={width}
            height={height}
            className="absolute top-0 left-0 w-full h-full pointer-events-none"
        />
    );
};
