'use client';

import React from 'react';
import { useRouter } from 'next/navigation';
import { usePatientStore } from '@/stores/usePatientStore';
import { Heading, Subheading, Body } from '@/components/shared/Typography';
import { Button } from '@/components/shared/Button';
import { Card } from '@/components/shared/Card';
import { ROMGauge } from '@/components/assessment/ROMGauge';
import { JointHighlight } from '@/components/assessment/JointHighlight';

export default function AssessmentPage() {
    const router = useRouter();
    const { patient, assessment } = usePatientStore();

    // Mock assessment data if none exists
    const displayAssessment = assessment || {
        patient_id: 'patient123',
        condition: 'Post-Elbow Fracture Stiffness',
        affected_joint: 'elbow',
        rom_deficit: 35,
        risk_level: 'moderate',
        summary_text: "Based on your clinical report and assessment, you're showing signed of 'Post-Elbow Fracture Stiffness'. This is common and highly responsive to targeted range-of-motion exercises. We've designed a specialized plan to regain those final 35 degrees of extension."
    };

    const riskColors = {
        low: 'bg-success/10 text-success border-success/20',
        moderate: 'bg-amber/10 text-amber border-amber/20',
        high: 'bg-danger/10 text-danger border-danger/20',
    };

    return (
        <main className="min-h-screen bg-background pt-12 pb-24">
            <div className="container mx-auto px-4 max-w-6xl">
                <div className="mb-12 text-center md:text-left">
                    <Heading>Assessment Results</Heading>
                    <Subheading>Welcome back, {patient?.name || 'Patient'}. Here is our clinical analysis.</Subheading>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
                    {/* Left Panel - Visuals */}
                    <div className="lg:col-span-5 space-y-8">
                        <JointHighlight joint={displayAssessment.affected_joint} />
                        <Card className="flex justify-around items-center py-10">
                            <ROMGauge current={110} target={145} label="Flexion" />
                            <div className="h-16 w-px bg-navy/10" />
                            <ROMGauge current={-15} target={0} label="Extension" />
                        </Card>
                    </div>

                    {/* Right Panel - Info */}
                    <div className="lg:col-span-7 space-y-8">
                        <Card variant="lg" className="space-y-8">
                            <div className="flex flex-wrap items-center justify-between gap-4">
                                <div className="space-y-1">
                                    <span className="text-xs uppercase tracking-widest font-bold text-navy/40">Clinical Diagnosis</span>
                                    <Heading level={3}>{displayAssessment.condition}</Heading>
                                </div>
                                <div className={`px-4 py-1 rounded-full border text-sm font-bold uppercase tracking-widest ${riskColors[displayAssessment.risk_level]}`}>
                                    {displayAssessment.risk_level} Risk
                                </div>
                            </div>

                            <div className="space-y-4">
                                <Body size="lg" className="leading-relaxed">
                                    {displayAssessment.summary_text}
                                </Body>
                            </div>

                            <div className="pt-6 border-t border-navy/5 space-y-4">
                                <span className="text-xs uppercase tracking-widest font-bold text-navy/40">Focus Areas</span>
                                <div className="flex flex-wrap gap-2">
                                    {['Passive Extension', 'Joint Mobilization', 'Strength Recovery'].map(f => (
                                        <span key={f} className="px-4 py-2 bg-navy/5 rounded-xl text-sm font-medium text-navy/70">
                                            {f}
                                        </span>
                                    ))}
                                </div>
                            </div>

                            <div className="pt-8">
                                <Button size="lg" className="w-full" onClick={() => router.push('/exercise')}>
                                    Start My Exercise Plan →
                                </Button>
                            </div>
                        </Card>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <Card variant="sm" className="flex items-center space-x-4">
                                <span className="text-2xl">📅</span>
                                <div>
                                    <div className="text-sm font-bold text-navy uppercase tracking-widest">Duration</div>
                                    <div className="text-navy/60">Estimated 6-8 weeks</div>
                                </div>
                            </Card>
                            <Card variant="sm" className="flex items-center space-x-4">
                                <span className="text-2xl">🔥</span>
                                <div>
                                    <div className="text-sm font-bold text-navy uppercase tracking-widest">Sets / Day</div>
                                    <div className="text-navy/60">3 targeted sessions</div>
                                </div>
                            </Card>
                        </div>
                    </div>
                </div>
            </div>
        </main>
    );
}
