'use client';

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { usePatientStore } from '@/stores/usePatientStore';
import { StepIndicator } from '@/components/shared/StepIndicator';
import { Button } from '@/components/shared/Button';
import { PersonalInfo } from './PersonalInfo';
import { IssueSelector } from './IssueSelector';
import { PainAssessment } from './PainAssessment';
import { MedicalUpload } from './MedicalUpload';

export const PatientForm: React.FC = () => {
    const [step, setStep] = useState(1);
    const totalSteps = 4;
    const { setPatient } = usePatientStore();

    const nextStep = () => setStep((s) => Math.min(s + 1, totalSteps));
    const prevStep = () => setStep((s) => Math.max(s - 1, 1));
    const finishOnboarding = () => {
        // In a real app, we'd save the form data here
        window.location.href = '/assessment';
    };

    const variants = {
        initial: { x: 50, opacity: 0 },
        animate: { x: 0, opacity: 1 },
        exit: { x: -50, opacity: 0 },
    };

    return (
        <div className="max-w-4xl mx-auto px-4 py-12">
            <div className="flex justify-between items-center mb-12">
                <StepIndicator currentStep={step} totalSteps={totalSteps} />
                {step > 1 && (
                    <Button variant="ghost" onClick={prevStep}>
                        Back
                    </Button>
                )}
            </div>

            <AnimatePresence mode="wait">
                <motion.div
                    key={step}
                    initial="initial"
                    animate="animate"
                    exit="exit"
                    variants={variants}
                    transition={{ duration: 0.4, ease: "easeOut" }}
                >
                    {step === 1 && <PersonalInfo onNext={nextStep} />}
                    {step === 2 && <IssueSelector onNext={nextStep} />}
                    {step === 3 && <PainAssessment onNext={nextStep} />}
                    {step === 4 && <MedicalUpload onComplete={finishOnboarding} onSkip={finishOnboarding} />}
                </motion.div>
            </AnimatePresence>
        </div>
    );
};
