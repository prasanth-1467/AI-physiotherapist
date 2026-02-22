'use client';

import React, { useRef, useState, useEffect } from 'react';
import { useWebcam } from '@/hooks/useWebcam';
import { usePoseDetection } from '@/hooks/usePoseDetection';
import { PoseOverlay } from './PoseOverlay';
import { Card } from '@/components/shared/Card';

interface CameraViewProps {
    onPoseResults?: (results: any) => void;
}

export const CameraView: React.FC<CameraViewProps> = ({ onPoseResults }) => {
    const { videoRef, isReady, error } = useWebcam();
    const results = usePoseDetection(videoRef);

    const [dimensions, setDimensions] = useState({ width: 0, height: 0 });
    const containerRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (results && onPoseResults) {
            onPoseResults(results);
        }
    }, [results, onPoseResults]);

    useEffect(() => {
        const updateDimensions = () => {
            if (containerRef.current) {
                setDimensions({
                    width: containerRef.current.clientWidth,
                    height: containerRef.current.clientHeight,
                });
            }
        };

        updateDimensions();
        window.addEventListener('resize', updateDimensions);
        return () => window.removeEventListener('resize', updateDimensions);
    }, []);

    return (
        <div ref={containerRef} className="relative w-full h-full min-h-[500px] bg-navy rounded-3xl overflow-hidden shadow-2xl">
            {!isReady && !error && (
                <div className="absolute inset-0 flex flex-col items-center justify-center text-white space-y-4">
                    <div className="w-12 h-12 border-4 border-teal border-t-transparent rounded-full animate-spin" />
                    <p className="font-body opacity-60">Initializing clinical camera...</p>
                </div>
            )}

            {error && (
                <div className="absolute inset-0 flex flex-col items-center justify-center text-white p-8 text-center space-y-4">
                    <span className="text-4xl">⚠️</span>
                    <p className="font-display text-xl">{error}</p>
                </div>
            )}

            <video
                ref={videoRef}
                className="w-full h-full object-cover mirror"
                playsInline
                muted
            />

            <PoseOverlay results={results} width={dimensions.width} height={dimensions.height} />

            {/* Mirror Effect CSS */}
            <style jsx>{`
        .mirror {
          transform: scaleX(-1);
        }
      `}</style>
        </div>
    );
};
