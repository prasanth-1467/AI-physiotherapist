import React from 'react';

interface CardProps {
    children: React.ReactNode;
    variant?: 'sm' | 'md' | 'lg';
    className?: string;
}

export const Card: React.FC<CardProps> = ({
    children,
    variant = 'md',
    className = '',
}) => {
    const paddings = {
        sm: 'p-4',
        md: 'p-6',
        lg: 'p-10',
    };

    return (
        <div className={`bg-white rounded-3xl shadow-sm border border-navy/5 ${paddings[variant]} ${className}`}>
            {children}
        </div>
    );
};
