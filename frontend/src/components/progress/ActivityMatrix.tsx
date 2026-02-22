'use client';

import React from 'react';

// Mock data for a month generated outside to be pure
const MOCK_DAYS = Array.from({ length: 30 }).map((_, i) => ({
    day: i + 1,
    status: Math.random() > 0.3 ? (Math.random() > 0.5 ? 'full' : 'partial') : 'none'
}));

const COLORS = {
    full: 'bg-teal',
    partial: 'bg-teal/30',
    none: 'bg-navy/5',
};

export const ActivityMatrix: React.FC = () => {
    return (
        <div className="space-y-4">
            <div className="flex justify-between items-center">
                <span className="text-xs uppercase tracking-widest font-bold text-navy/40">Last 30 Days</span>
                <div className="flex space-x-4 text-[10px] uppercase tracking-widest font-bold text-navy/40">
                    <div className="flex items-center space-x-1">
                        <div className="w-2 h-2 rounded-sm bg-navy/5" />
                        <span>Rest</span>
                    </div>
                    <div className="flex items-center space-x-1">
                        <div className="w-2 h-2 rounded-sm bg-teal/30" />
                        <span>Partial</span>
                    </div>
                    <div className="flex items-center space-x-1">
                        <div className="w-2 h-2 rounded-sm bg-teal" />
                        <span>Complete</span>
                    </div>
                </div>
            </div>
            <div className="grid grid-cols-10 gap-2">
                {MOCK_DAYS.map((d) => (
                    <div
                        key={d.day}
                        className={`aspect-square rounded-md ${COLORS[d.status as keyof typeof COLORS]} transition-all hover:scale-110 cursor-pointer`}
                        title={`Day ${d.day}`}
                    />
                ))}
            </div>
        </div>
    );
};
