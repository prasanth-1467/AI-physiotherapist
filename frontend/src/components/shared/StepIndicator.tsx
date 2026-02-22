import React from 'react';

interface StepIndicatorProps {
    currentStep: number;
    totalSteps: number;
}

export const StepIndicator: React.FC<StepIndicatorProps> = ({ currentStep, totalSteps }) => {
    return (
        <div className="flex items-center space-x-4">
            {Array.from({ length: totalSteps }).map((_, i) => (
                <div
                    key={i}
                    className={`h-2 transition-all duration-300 rounded-full ${i + 1 === currentStep
                            ? 'w-8 bg-teal'
                            : i + 1 < currentStep
                                ? 'w-2 bg-success'
                                : 'w-2 bg-navy/10'
                        }`}
                />
            ))}
        </div>
    );
};
