'use client';

import { useEffect, useRef, useState, useCallback } from 'react';
import { PoseLandmarker, FilesetResolver, PoseLandmarkerResult } from '@mediapipe/tasks-vision';

export const usePoseDetection = (videoRef: React.RefObject<HTMLVideoElement | null>) => {
    const [results, setResults] = useState<PoseLandmarkerResult | null>(null);
    const poseLandmarkerRef = useRef<PoseLandmarker | null>(null);

    const createPoseLandmarker = useCallback(async () => {
        const vision = await FilesetResolver.forVisionTasks(
            "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@latest/wasm"
        );
        poseLandmarkerRef.current = await PoseLandmarker.createFromOptions(vision, {
            baseOptions: {
                modelAssetPath: `https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/1/pose_landmarker_lite.task`,
                delegate: "GPU"
            },
            runningMode: "VIDEO",
            numPoses: 1
        });
    }, []);

    useEffect(() => {
        createPoseLandmarker();
        return () => {
            poseLandmarkerRef.current?.close();
        };
    }, [createPoseLandmarker]);

    const detect = useCallback(() => {
        if (
            videoRef.current &&
            poseLandmarkerRef.current &&
            videoRef.current.readyState === 4
        ) {
            const startTimeMs = performance.now();
            const poseResult = poseLandmarkerRef.current.detectForVideo(videoRef.current, startTimeMs);
            setResults(poseResult);
        }
    }, [videoRef]);

    useEffect(() => {
        let animationFrameId: number;

        const runDetection = () => {
            detect();
            animationFrameId = requestAnimationFrame(runDetection);
        };

        runDetection();

        return () => {
            cancelAnimationFrame(animationFrameId);
        };
    }, [detect]);

    return results;
};
