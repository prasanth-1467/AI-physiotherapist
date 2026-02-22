'use client';

import React from 'react';
import { useRouter } from 'next/navigation';
import { Heading, Subheading, Body } from '@/components/shared/Typography';
import { Button } from '@/components/shared/Button';
import { Card } from '@/components/shared/Card';
import { RecoveryChart } from '@/components/progress/RecoveryChart';

export default function SessionSummaryPage() {
    const router = useRouter();

    const stats = [
        { label: 'Exercises', value: '3', unit: 'Items', icon: '🎯' },
        { label: 'Time Spent', value: '18', unit: 'Mins', icon: '⏱️' },
        { label: 'Accuracy', value: '92', unit: '%', icon: '✨' },
        { label: 'REPS', value: '36', unit: 'Total', icon: '💪' },
    ];

    return (
        <main className="min-h-screen bg-background pt-12 pb-24">
            <div className="container mx-auto px-4 max-w-5xl space-y-12">
                <div className="text-center space-y-4">
                    <div className="inline-flex items-center space-x-2 px-4 py-2 bg-success/10 text-success rounded-full text-sm font-bold uppercase tracking-widest">
                        <span>✓</span>
                        <span>Session Complete</span>
                    </div>
                    <Heading>Incredible effort today!</Heading>
                    <Subheading>You&apos;re only 12% away from your full range-of-motion target.</Subheading>
                </div>

                <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
                    {stats.map((stat) => (
                        <Card key={stat.label} variant="sm" className="text-center space-y-2">
                            <span className="text-3xl block mb-2">{stat.icon}</span>
                            <div className="text-2xl font-display text-navy leading-none">
                                {stat.value}
                                <span className="text-sm font-body text-navy/40 ml-1">{stat.unit}</span>
                            </div>
                            <span className="text-xs uppercase tracking-widest font-bold text-navy/40 block">
                                {stat.label}
                            </span>
                        </Card>
                    ))}
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
                    <Card variant="lg" className="lg:col-span-8 flex flex-col justify-between">
                        <div className="mb-8">
                            <Heading level={3}>Recovery Progress</Heading>
                            <Body>Your extension has improved by 4° since last week.</Body>
                        </div>
                        <RecoveryChart />
                    </Card>

                    <Card variant="lg" className="lg:col-span-4 space-y-8">
                        <Heading level={3}>Next Steps</Heading>
                        <div className="space-y-6">
                            {[
                                { title: 'Ice Therapy', desc: '10 mins on the joint', icon: '❄️' },
                                { title: 'Hydration', desc: 'Drink 500ml water', icon: '💧' },
                                { title: 'Rest Period', desc: 'Next session in 4h', icon: '🛌' },
                            ].map((step) => (
                                <div key={step.title} className="flex items-start space-x-4">
                                    <span className="text-2xl mt-1">{step.icon}</span>
                                    <div>
                                        <div className="font-bold text-navy leading-tight">{step.title}</div>
                                        <Body size="base" className="text-sm">{step.desc}</Body>
                                    </div>
                                </div>
                            ))}
                        </div>
                        <div className="pt-6 border-t border-navy/5">
                            <Button size="lg" className="w-full" onClick={() => router.push('/progress')}>
                                View Full History
                            </Button>
                        </div>
                    </Card>
                </div>

                <div className="flex justify-center pt-8">
                    <Button variant="ghost" onClick={() => router.push('/')}>
                        Return to Dashboard
                    </Button>
                </div>
            </div>
        </main>
    );
}
