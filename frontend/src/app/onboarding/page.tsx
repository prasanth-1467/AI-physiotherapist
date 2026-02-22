'use client';

import React from 'react';
import { PatientForm } from '@/components/onboarding/PatientForm';

export default function OnboardingPage() {
    return (
        <main className="min-h-screen bg-background pt-8">
            <div className="container mx-auto">
                <PatientForm />
            </div>
        </main>
    );
}
