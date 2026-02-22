'use client';

import React from 'react';
import { useRouter } from 'next/navigation';
import { Heading, Subheading, Body } from '@/components/shared/Typography';
import { Button } from '@/components/shared/Button';
import { Card } from '@/components/shared/Card';
import { RecoveryChart } from '@/components/progress/RecoveryChart';
import { ActivityMatrix } from '@/components/progress/ActivityMatrix';

export default function ProgressPage() {
    const router = useRouter();

    const sessions = [
        { date: 'Oct 24, 2023', exercise: 'T-Pose Extension', accuracy: '94%', duration: '12m' },
        { date: 'Oct 23, 2023', exercise: 'Elbow Flexion', accuracy: '89%', duration: '15m' },
        { date: 'Oct 22, 2023', exercise: 'Shoulder Press', accuracy: '91%', duration: '10m' },
        { date: 'Oct 21, 2023', exercise: 'T-Pose Extension', accuracy: '92%', duration: '14m' },
    ];

    return (
        <main className="min-h-screen bg-background pt-12 pb-24">
            <div className="container mx-auto px-4 max-w-6xl space-y-12">
                <div className="flex flex-col md:flex-row md:items-end justify-between gap-6">
                    <div className="space-y-2">
                        <Heading>My Progress</Heading>
                        <Subheading>Tracking your journey since October 12, 2023</Subheading>
                    </div>
                    <Button size="lg" onClick={() => router.push('/exercise')}>
                        Start Today&apos;s Session
                    </Button>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
                    {/* Main Chart Section */}
                    <div className="lg:col-span-8 space-y-8">
                        <Card variant="lg" className="space-y-8">
                            <div className="flex justify-between items-center">
                                <div>
                                    <span className="text-xs uppercase tracking-widest font-bold text-navy/40">Recovery Trend</span>
                                    <Heading level={3}>Range of Motion</Heading>
                                </div>
                                <div className="text-right">
                                    <div className="text-3xl font-display text-teal">+12°</div>
                                    <div className="text-xs font-bold text-navy/40 uppercase">Total Improvement</div>
                                </div>
                            </div>
                            <RecoveryChart />
                        </Card>

                        <Card variant="lg" className="space-y-6">
                            <Heading level={3}>Recent Sessions</Heading>
                            <div className="overflow-x-auto">
                                <table className="w-full">
                                    <thead>
                                        <tr className="border-b border-navy/5 text-left">
                                            <th className="pb-4 text-xs font-bold text-navy/30 uppercase tracking-widest">Date</th>
                                            <th className="pb-4 text-xs font-bold text-navy/30 uppercase tracking-widest">Exercise</th>
                                            <th className="pb-4 text-xs font-bold text-navy/30 uppercase tracking-widest text-center">Accuracy</th>
                                            <th className="pb-4 text-xs font-bold text-navy/30 uppercase tracking-widest text-right">Time</th>
                                        </tr>
                                    </thead>
                                    <tbody className="divide-y divide-navy/5 font-body">
                                        {sessions.map((s, i) => (
                                            <tr key={i} className="group hover:bg-navy/[0.02] transition-colors">
                                                <td className="py-4 text-navy/70 font-medium">{s.date}</td>
                                                <td className="py-4 text-navy font-bold">{s.exercise}</td>
                                                <td className="py-4 text-center">
                                                    <span className="px-3 py-1 bg-teal/10 text-teal rounded-full text-xs font-bold">
                                                        {s.accuracy}
                                                    </span>
                                                </td>
                                                <td className="py-4 text-right text-navy/50">{s.duration}</td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        </Card>
                    </div>

                    {/* Sidebar Section */}
                    <div className="lg:col-span-4 space-y-8">
                        <Card variant="md" className="space-y-6">
                            <Heading level={3}>Compliance</Heading>
                            <ActivityMatrix />
                            <div className="pt-4 space-y-2">
                                <div className="flex justify-between text-sm">
                                    <span className="text-navy/60">Consistency Score</span>
                                    <span className="font-bold text-navy">85%</span>
                                </div>
                                <div className="w-full h-1 bg-navy/5 rounded-full">
                                    <div className="h-full bg-teal w-[85%] rounded-full" />
                                </div>
                            </div>
                        </Card>

                        <Card variant="md" className="bg-navy text-white space-y-6">
                            <div className="space-y-2">
                                <span className="text-xs uppercase tracking-widest font-bold opacity-40">Pro Insight</span>
                                <Heading level={3} className="text-white">Keep it up!</Heading>
                            </div>
                            <Body className="text-white/70 text-sm italic">
                                &quot;We&apos;re seeing significant improvement in your extension. Your consistency this week has been excellent. Focus on controlled movements tomorrow.&quot;
                            </Body>
                            <div className="flex items-center space-x-3">
                                <div className="w-10 h-10 rounded-full bg-teal/20 flex items-center justify-center text-xl">👩‍⚕️</div>
                                <div>
                                    <div className="text-sm font-bold">Dr. Sarah Chen</div>
                                    <div className="text-xs opacity-50">Lead Physiotherapist</div>
                                </div>
                            </div>
                        </Card>
                    </div>
                </div>
            </div>
        </main>
    );
}
