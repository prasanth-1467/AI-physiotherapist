import React from 'react';

interface RepCounterProps {
    current: number;
    total: number;
}

export const RepCounter: React.FC<RepCounterProps> = ({ current, total }) => {
    return (
        <div className="flex flex-col items-center justify-center space-y-2">
            <div className="text-[120px] leading-none font-display text-teal tabular-nums">
                {current}
            </div>
            <div className="px-6 py-2 bg-teal/10 rounded-full">
                <span className="text-sm font-bold text-teal uppercase tracking-widest">
                    / {total} Reps
                </span>
            </div>
        </div>
    );
};
