import React from 'react';
import { Card } from '@/components/shared/Card';
import { Button } from '@/components/shared/Button';
import { Heading, Subheading, Body } from '@/components/shared/Typography';

interface PainAssessmentProps {
    onNext: () => void;
}

export const PainAssessment: React.FC<PainAssessmentProps> = ({ onNext }) => {
    return (
        <div className="space-y-8">
            <Heading>Pain Assessment</Heading>
            <Subheading>How are you feeling today? Use the slider below to indicate your pain level.</Subheading>

            <Card variant="lg" className="space-y-12">
                <div className="space-y-8">
                    <div className="flex justify-between text-4xl">
                        <span>😀</span>
                        <span>😐</span>
                        <span>😫</span>
                    </div>
                    <input type="range" min="0" max="10" className="w-full accent-teal h-2 bg-navy/10 rounded-full appearance-none cursor-pointer" />
                    <div className="flex justify-between font-medium text-navy/40 px-2">
                        <span>0 - No Pain</span>
                        <span>10 - Severe Pain</span>
                    </div>
                </div>

                <div className="space-y-4">
                    <Body className="font-semibold">Are there any specific limitations?</Body>
                    <div className="space-y-3">
                        {['Lifting arm', 'Bending elbow', 'Gripping objects', 'Walking'].map(q => (
                            <label key={q} className="flex items-center p-4 rounded-2xl bg-navy/5 border border-transparent hover:border-teal/30 cursor-pointer transition-all">
                                <input type="checkbox" className="w-5 h-5 accent-teal rounded-md" />
                                <span className="ml-4 font-medium text-navy">{q}</span>
                            </label>
                        ))}
                    </div>
                </div>

                <Button size="lg" className="w-full" onClick={onNext}>
                    Continue
                </Button>
            </Card>
        </div>
    );
};
