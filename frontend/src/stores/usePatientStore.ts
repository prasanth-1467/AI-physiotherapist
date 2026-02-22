import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { PatientInfo, AssessmentResult, ExercisePlan, SessionState } from '@/types/patient';

interface PatientStore {
    patient: PatientInfo | null;
    assessment: AssessmentResult | null;
    exercisePlan: ExercisePlan | null;
    currentSession: SessionState | null;

    setPatient: (patient: PatientInfo) => void;
    setAssessment: (assessment: AssessmentResult) => void;
    setExercisePlan: (plan: ExercisePlan) => void;
    startSession: (session: SessionState) => void;
    endSession: () => void;
    reset: () => void;
}

export const usePatientStore = create<PatientStore>()(
    persist(
        (set) => ({
            patient: null,
            assessment: null,
            exercisePlan: null,
            currentSession: null,

            setPatient: (patient) => set({ patient }),
            setAssessment: (assessment) => set({ assessment }),
            setExercisePlan: (exercisePlan) => set({ exercisePlan }),
            startSession: (currentSession) => set({ currentSession }),
            endSession: () => set({ currentSession: null }),
            reset: () => set({ patient: null, assessment: null, exercisePlan: null, currentSession: null }),
        }),
        {
            name: 'physio-patient-storage',
        }
    )
);
