export type SubjectId =
  | "math"
  | "physics"
  | "informatics"
  | "english"
  | "russian"
  | "chemistry"
  | "biology"
  | "history"
  | "custom";

export interface Subject {
  id: SubjectId;
  name: string;
  category: string;
  badge: string;
  iconName: string;
  description: string;
  accent: {
    bg: string;
    text: string;
    border: string;
    gradient: string;
  };
  sampleTopics: string[];
}

export type TutorMode =
  | "socratic"
  | "expert"
  | "solver"
  | "quiz"
  | "flashcards"
  | "concept"
  | "plan";

export type TutorTone =
  | "encouraging"
  | "strict"
  | "friendly_peer"
  | "olympiad";

export type UserLevel =
  | "5-8 класс (База)"
  | "9 класс (ОГЭ)"
  | "10-11 класс (ЕГЭ/ЦТ)"
  | "Студент ВУЗа"
  | "С нуля для взрослых";

export interface ChatMessage {
  id: string;
  role: "user" | "model";
  text: string;
  timestamp: number;
  imageBase64?: string;
  isStreaming?: boolean;
}

export interface QuizQuestion {
  question: string;
  options: string[];
  correctIndex: number;
  explanation: string;
  hint: string;
  difficulty: string;
}

export interface Flashcard {
  id: string;
  front: string;
  back: string;
  mnemonic: string;
  category: string;
  status?: "new" | "learned" | "review";
}

export interface StudyModule {
  weekNumber: number;
  title: string;
  objectives: string[];
  practiceTask: string;
  selfCheckQuestion: string;
}

export interface StudyPlan {
  title: string;
  estimatedTotalHours: number;
  overview: string;
  modules: StudyModule[];
  tips: string[];
}

export interface ConceptExplanation {
  concept: string;
  simple: string;
  academic: string;
  realLife: string;
  quickQuestion: string;
}

export interface UserStats {
  xp: number;
  streakDays: number;
  lessonsDone: number;
  quizzesTaken: number;
  cardsMastered: number;
  recentNotes: { id: string; date: string; title: string; preview: string }[];
}
