import React from 'react';

interface JointHighlightProps {
    joint: string; // e.g., 'elbow', 'shoulder', 'knee'
}

export const JointHighlight: React.FC<JointHighlightProps> = ({ joint }) => {
    return (
        <div className="relative w-full max-w-sm mx-auto aspect-[1/2] bg-navy/5 rounded-3xl p-8 flex items-center justify-center overflow-hidden">
            {/* Simple SVG Human Outline */}
            <svg viewBox="0 0 100 200" className="w-full h-full text-navy/10 fill-current">
                <circle cx="50" cy="20" r="15" /> {/* Head */}
                <path d="M50 35 L50 100 M20 50 L80 50 M20 50 L20 80 M80 50 L80 80 M50 100 L30 160 M50 100 L70 160" stroke="currentColor" strokeWidth="8" strokeLinecap="round" />

                {/* Highlight based on joint */}
                {joint === 'elbow' && (
                    <g>
                        <circle cx="20" cy="65" r="8" className="text-amber fill-current animate-pulse" />
                        <circle cx="20" cy="65" r="12" className="text-amber/30 fill-transparent stroke-current stroke-2 animate-ping" />
                    </g>
                )}
                {joint === 'shoulder' && (
                    <g>
                        <circle cx="35" cy="50" r="8" className="text-amber fill-current animate-pulse" />
                        <circle cx="35" cy="50" r="12" className="text-amber/30 fill-transparent stroke-current stroke-2 animate-ping" />
                    </g>
                )}
            </svg>

            <div className="absolute bottom-6 left-6 right-6 p-4 bg-white/80 backdrop-blur-sm rounded-2xl border border-navy/5">
                <span className="text-xs uppercase tracking-widest font-bold text-navy/40 block mb-1">Focus Area</span>
                <span className="text-lg font-display text-navy capitalize">{joint} Joint</span>
            </div>
        </div>
    );
};
