'use client';

import { useState, useCallback, useRef } from 'react';

export const useRepCounter = (targetAngle: number, threshold: number = 15) => {
    const [reps, setReps] = useState(0);
    const [feedback, setFeedback] = useState<string | null>(null);
    const stageRef = useRef<'up' | 'down'>('down');

    const updateReps = useCallback((currentAngle: number) => {
        const diff = Math.abs(currentAngle - targetAngle);

        if (diff < 10) {
            if (stageRef.current === 'down') {
                stageRef.current = 'up';
            }
        }

        if (diff > threshold && stageRef.current === 'up') {
            stageRef.current = 'down';
            setReps((r) => r + 1);
            setFeedback('Great work! Keep it up.');
            setTimeout(() => setFeedback(null), 3000);
        }

        // Corrective feedback
        if (diff > threshold * 2) {
            setFeedback('Try to reach the target angle further');
        }
    }, [targetAngle, threshold]);

    return { reps, feedback, updateReps };
};
