import React from 'react';

interface ROMGaugeProps {
    current: number;
    target: number;
    label: string;
}

export const ROMGauge: React.FC<ROMGaugeProps> = ({ current, target, label }) => {
    const percentage = Math.min((current / target) * 100, 100);
    const radius = 80;
    const circumference = 2 * Math.PI * radius;
    const offset = circumference - (percentage / 100) * circumference;

    return (
        <div className="flex flex-col items-center space-y-4">
            <div className="relative w-48 h-48">
                {/* Background circle */}
                <svg className="w-full h-full transform -rotate-90">
                    <circle
                        cx="96"
                        cy="96"
                        r={radius}
                        stroke="currentColor"
                        strokeWidth="12"
                        fill="transparent"
                        className="text-navy/5"
                    />
                    {/* Progress circle */}
                    <circle
                        cx="96"
                        cy="96"
                        r={radius}
                        stroke="currentColor"
                        strokeWidth="12"
                        strokeDasharray={circumference}
                        strokeDashoffset={offset}
                        strokeLinecap="round"
                        fill="transparent"
                        className="text-teal transition-all duration-1000 ease-out"
                    />
                </svg>
                <div className="absolute inset-0 flex flex-col items-center justify-center">
                    <span className="text-4xl font-display text-navy">{current}°</span>
                    <span className="text-sm font-body text-navy/40">Target {target}°</span>
                </div>
            </div>
            <span className="text-lg font-body font-medium text-navy">{label}</span>
        </div>
    );
};
