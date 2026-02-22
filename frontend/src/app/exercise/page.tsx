'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { usePatientStore } from '@/stores/usePatientStore';
import { CameraView } from '@/components/exercise/CameraView';
import { AngleMeter } from '@/components/exercise/AngleMeter';
import { RepCounter } from '@/components/exercise/RepCounter';
import { CorrectionBanner } from '@/components/exercise/CorrectionBanner';
import { Heading, Body } from '@/components/shared/Typography';
import { Button } from '@/components/shared/Button';
import { Card } from '@/components/shared/Card';
import { getJointAngles } from '@/lib/angleUtils';
import { useRepCounter } from '@/hooks/useRepCounter';
import { PoseLandmarkerResult } from '@mediapipe/tasks-vision';

export default function ExercisePage() {
    const router = useRouter();
    const { patient, exercisePlan } = usePatientStore();
    const [currentAngle, setCurrentAngle] = useState(0);

    // Mock plan if none
    const plan = exercisePlan || {
        exercise: 'T-Pose Extension',
        target_angle: 180,
        reps: 12,
        sets: 3,
        hold_seconds: 0
    };

    const { reps, feedback, updateReps } = useRepCounter(plan.target_angle);

    const handlePoseResults = (results: PoseLandmarkerResult) => {
        if (results && results.landmarks && results.landmarks.length > 0) {
            const landmarks = results.landmarks[0];
            const angles = getJointAngles(landmarks);
            if (angles) {
                // Assume we track right elbow for T-pose extension if affected joint is elbow
                const angle = angles.right_elbow;
                setCurrentAngle(angle);
                updateReps(angle);
            }
        }
    };

    useEffect(() => {
        if (reps >= plan.reps) {
            // Session complete logic or next set
            setTimeout(() => {
                router.push('/session-summary');
            }, 2000);
        }
    }, [reps, plan.reps, router]);

    return (
        <main className="min-h-screen bg-background p-4 md:p-8">
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 h-[calc(100vh-64px)] overflow-hidden">

                {/* Left Panel - Live Stream */}
                <div className="lg:col-span-8 relative">
                    <CameraView onPoseResults={handlePoseResults} />
                    <CorrectionBanner message={feedback} />
                </div>

                {/* Right Panel - Feedback & Controls */}
                <div className="lg:col-span-4 flex flex-col space-y-6 overflow-y-auto pr-2">

                    <Card variant="md" className="space-y-2">
                        <span className="text-xs uppercase tracking-widest font-bold text-navy/40">Current Exercise</span>
                        <Heading level={3}>{plan.exercise}</Heading>
                        <Body className="text-sm">Keep your back straight and extend your arm fully to the side.</Body>
                    </Card>

                    <div className="grid grid-cols-2 gap-4">
                        <Card className="flex flex-col items-center justify-center py-8">
                            <RepCounter current={reps} total={plan.reps} />
                        </Card>
                        <Card className="flex flex-col items-center justify-center py-8">
                            <AngleMeter angle={currentAngle} target={plan.target_angle} />
                        </Card>
                    </div>

                    <Card variant="md" className="flex-grow space-y-6">
                        <div className="space-y-4">
                            <span className="text-xs uppercase tracking-widest font-bold text-navy/40">Instructions</span>
                            <ul className="space-y-3">
                                {[
                                    'Stand with feet shoulder-width apart',
                                    'Raise arms to shoulder height',
                                    'Fingertips reaching outward',
                                    'Hold for 2 seconds at full extension'
                                ].map((inst, i) => (
                                    <li key={i} className="flex items-start">
                                        <span className="w-5 h-5 rounded-full bg-teal/10 text-teal text-xs flex items-center justify-center font-bold mr-3 mt-1">
                                            {i + 1}
                                        </span>
                                        <span className="text-navy/70 text-sm leading-relaxed">{inst}</span>
                                    </li>
                                ))}
                            </ul>
                        </div>

                        <div className="pt-6 border-t border-navy/5">
                            <div className="flex justify-between items-center mb-2">
                                <span className="text-xs uppercase tracking-widest font-bold text-navy/40">Session Progress</span>
                                <span className="text-xs font-bold text-teal">Set 1 of {plan.sets}</span>
                            </div>
                            <div className="w-full h-2 bg-navy/5 rounded-full overflow-hidden">
                                <div
                                    className="h-full bg-teal transition-all duration-500 ease-out"
                                    style={{ width: `${(reps / plan.reps) * 100}%` }}
                                />
                            </div>
                        </div>

                        <div className="pt-4 flex gap-3">
                            <Button variant="secondary" className="flex-1" onClick={() => router.push('/assessment')}>
                                End Early
                            </Button>
                            <Button variant="ghost" className="px-4">
                                Mute
                            </Button>
                        </div>
                    </Card>

                </div>
            </div>
        </main>
    );
}
