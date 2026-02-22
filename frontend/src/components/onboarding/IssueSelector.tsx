import React from 'react';
import { Heading, Subheading } from '@/components/shared/Typography';

interface IssueSelectorProps {
    onNext: () => void;
}

export const IssueSelector: React.FC<IssueSelectorProps> = ({ onNext }) => {
    const issues = [
        { id: 'fracture', label: 'Bone Fracture', icon: '🦴' },
        { id: 'sprain', label: 'Muscle Sprain', icon: '💪' },
        { id: 'surgery', label: 'Post-Surgery', icon: '🔩' },
        { id: 'stroke', label: 'Stroke Rehab', icon: '🧠' },
        { id: 'knee', label: 'Knee Injury', icon: '🦵' },
        { id: 'frozen', label: 'Frozen Shoulder', icon: '🪨' },
    ];

    return (
        <div className="space-y-8">
            <Heading>What's the concern?</Heading>
            <Subheading>Select the condition or area you'd like to focus on for your rehabilitation.</Subheading>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {issues.map((item) => (
                    <button
                        key={item.id}
                        className="group bg-white p-6 rounded-3xl border-2 border-transparent hover:border-teal/30 hover:shadow-md transition-all text-left"
                        onClick={onNext}
                    >
                        <span className="text-4xl mb-4 block group-hover:scale-110 transition-transform">{item.icon}</span>
                        <span className="text-lg font-body font-semibold text-navy block">{item.label}</span>
                    </button>
                ))}
            </div>
        </div>
    );
};
