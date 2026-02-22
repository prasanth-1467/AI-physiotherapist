import React from 'react';

interface AngleMeterProps {
    angle: number;
    target: number;
}

export const AngleMeter: React.FC<AngleMeterProps> = ({ angle, target }) => {
    const diff = Math.abs(angle - target);
    const isTarget = diff <= 5;
    const isClose = diff <= 15;

    let color = 'text-danger';
    if (isTarget) color = 'text-success';
    else if (isClose) color = 'text-amber';

    return (
        <div className="flex flex-col items-center space-y-4 text-center">
            <div className={`text-6xl font-display transition-colors duration-300 ${color}`}>
                {angle}°
            </div>
            <div className="space-y-1">
                <span className="text-xs uppercase tracking-widest font-bold text-navy/40 block">Current Angle</span>
                <span className="text-sm font-medium text-navy/60">Target: {target}°</span>
            </div>
        </div>
    );
};
