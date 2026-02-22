import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface CorrectionBannerProps {
    message: string | null;
}

export const CorrectionBanner: React.FC<CorrectionBannerProps> = ({ message }) => {
    return (
        <AnimatePresence>
            {message && (
                <motion.div
                    initial={{ y: 50, opacity: 0 }}
                    animate={{ y: 0, opacity: 1 }}
                    exit={{ y: 50, opacity: 0 }}
                    className="absolute bottom-12 left-1/2 -translate-x-1/2 z-50 px-8 py-4 bg-amber text-navy rounded-2xl shadow-2xl flex items-center space-x-4 border border-navy/10"
                    role="alert"
                >
                    <span className="text-2xl">⚠️</span>
                    <span className="font-body font-bold text-lg">{message}</span>
                </motion.div>
            )}
        </AnimatePresence>
    );
};
