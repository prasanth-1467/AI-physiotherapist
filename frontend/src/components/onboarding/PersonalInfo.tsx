import React from 'react';
import { Card } from '@/components/shared/Card';
import { Button } from '@/components/shared/Button';
import { Heading, Subheading } from '@/components/shared/Typography';

interface PersonalInfoProps {
    onNext: () => void;
}

export const PersonalInfo: React.FC<PersonalInfoProps> = ({ onNext }) => {
    return (
        <div className="space-y-8">
            <Heading>Welcome to PhysioAI</Heading>
            <Subheading>Let's start with some basic information to personalize your recovery plan.</Subheading>

            <Card variant="lg" className="space-y-6">
                <div className="space-y-2">
                    <label className="text-sm font-medium text-navy/60 ml-2">Full Name</label>
                    <input
                        type="text"
                        placeholder="Enter your full name"
                        className="w-full px-6 py-4 rounded-2xl border border-navy/10 focus:border-teal focus:ring-1 focus:ring-teal outline-none text-lg transition-all"
                    />
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="space-y-2">
                        <label className="text-sm font-medium text-navy/60 ml-2">Age</label>
                        <input
                            type="number"
                            min="18" max="99"
                            placeholder="e.g. 28"
                            className="w-full px-6 py-4 rounded-2xl border border-navy/10 focus:border-teal focus:ring-1 focus:ring-teal outline-none text-lg transition-all"
                        />
                    </div>
                    <div className="space-y-2">
                        <label className="text-sm font-medium text-navy/60 ml-2">Gender</label>
                        <div className="flex p-1 bg-navy/5 rounded-2xl">
                            {['Male', 'Female', 'Other'].map((g) => (
                                <button
                                    key={g}
                                    className="flex-1 py-3 rounded-xl text-md font-medium transition-all hover:bg-white/50 focus:bg-white active:bg-white"
                                >
                                    {g}
                                </button>
                            ))}
                        </div>
                    </div>
                </div>

                <Button size="lg" className="w-full mt-4" onClick={onNext}>
                    Next Step
                </Button>
            </Card>
        </div>
    );
};
