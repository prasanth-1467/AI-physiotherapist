import React from 'react';

interface TextProps {
    children: React.ReactNode;
    className?: string;
}

export const Heading: React.FC<TextProps & { level?: 1 | 2 | 3 }> = ({
    children,
    className = '',
    level = 1
}) => {
    const styles = {
        1: 'text-4xl md:text-5xl lg:text-6xl font-display text-navy mb-4 leading-tight',
        2: 'text-3xl md:text-4xl font-display text-navy mb-3',
        3: 'text-2xl md:text-3xl font-display text-navy mb-2',
    };

    const Tag = `h${level}` as keyof JSX.IntrinsicElements;
    return <Tag className={`${styles[level]} ${className}`}>{children}</Tag>;
};

export const Subheading: React.FC<TextProps> = ({ children, className = '' }) => (
    <h4 className={`text-xl md:text-2xl font-body font-medium text-navy/80 mb-4 ${className}`}>
        {children}
    </h4>
);

export const Body: React.FC<TextProps & { size?: 'base' | 'lg' }> = ({
    children,
    className = '',
    size = 'base'
}) => {
    const sizes = {
        base: 'text-accessible-base',
        lg: 'text-accessible-lg',
    };
    return <p className={`font-body text-navy/70 ${sizes[size]} ${className}`}>{children}</p>;
};

export const Caption: React.FC<TextProps> = ({ children, className = '' }) => (
    <span className={`text-sm font-body text-navy/50 uppercase tracking-wider ${className}`}>
        {children}
    </span>
);
