import React from 'react';
import { Card } from '@/components/shared/Card';
import { Button } from '@/components/shared/Button';
import { Heading, Subheading, Body } from '@/components/shared/Typography';

interface MedicalUploadProps {
    onComplete: () => void;
    onSkip: () => void;
}

export const MedicalUpload: React.FC<MedicalUploadProps> = ({ onComplete, onSkip }) => {
    return (
        <div className="space-y-8">
            <Heading>Medical Reports</Heading>
            <Subheading>Upload any recent medical reports or imaging (PDF/JPG) for a more accurate diagnosis.</Subheading>

            <Card variant="lg" className="space-y-8 border-2 border-dashed border-teal/30 bg-teal/5">
                <div className="py-12 flex flex-col items-center space-y-4">
                    <span className="text-6xl">📄</span>
                    <div className="text-center">
                        <Body className="font-medium">Drag and drop your report here</Body>
                        <Body className="text-navy/40 text-sm">or click to browse from your device</Body>
                    </div>
                    <Button variant="secondary">Browse Files</Button>
                </div>
            </Card>

            <div className="flex flex-col space-y-4">
                <Button size="lg" onClick={onComplete}>
                    Finish Onboarding
                </Button>
                <Button variant="ghost" onClick={onSkip}>
                    Skip for now
                </Button>
            </div>
        </div>
    );
};
