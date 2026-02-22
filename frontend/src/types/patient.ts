export type PatientInfo = {
    name: string;
    age: number;
    gender: string;
    conditions: string[];
    affectedSide: 'left' | 'right' | 'both';
    painLevel: number;
    limitedMovements: string[];
    conditionDuration: string;
    hasPriorPhysio: boolean;
    profileImage?: string;
};

export type AssessmentResult = {
    patient_id: string;
    condition: string;
    affected_joint: string;
    rom_deficit: number;
    risk_level: 'low' | 'moderate' | 'high';
    summary_text?: string;
};

export type ExercisePlan = {
    exercise: string;
    target_angle: number;
    reps: number;
    sets: number;
    hold_seconds: number;
};

export type SessionState = {
    sessionId: string;
    startTime: string;
    exercisesCompleted: string[];
};
