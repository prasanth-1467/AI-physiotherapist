'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { usePatientStore } from '@/stores/usePatientStore';
import { Button } from '@/components/shared/Button';
import { Heading, Body } from '@/components/shared/Typography';

export default function LandingPage() {
  const router = useRouter();
  const { patient } = usePatientStore();

  useEffect(() => {
    if (patient) {
      router.push('/exercise');
    }
  }, [patient, router]);

  return (
    <main className="min-h-screen flex flex-col items-center justify-center p-8 text-center space-y-8 max-w-2xl mx-auto">
      <div className="space-y-4">
        <Heading>Your Journey to Recovery Starts Here</Heading>
        <Body size="lg">
          PhysioAI combines advanced pose estimation with clinical expertise
          to guide you through your rehabilitation from the comfort of your home.
        </Body>
      </div>

      <div className="flex flex-col sm:flex-row gap-4 w-full sm:w-auto">
        <Button size="lg" onClick={() => router.push('/onboarding')}>
          Get Started
        </Button>
        <Button variant="secondary" size="lg">
          Learn More
        </Button>
      </div>

      <div className="pt-12 grid grid-cols-2 md:grid-cols-3 gap-8 opacity-50">
        <div className="space-y-1">
          <div className="text-2xl font-display">98%</div>
          <div className="text-xs uppercase tracking-widest font-bold">Accuracy</div>
        </div>
        <div className="space-y-1">
          <div className="text-2xl font-display">15+</div>
          <div className="text-xs uppercase tracking-widest font-bold">Joints</div>
        </div>
        <div className="hidden md:block space-y-1">
          <div className="text-2xl font-display">24/7</div>
          <div className="text-xs uppercase tracking-widest font-bold">Available</div>
        </div>
      </div>
    </main>
  );
}
