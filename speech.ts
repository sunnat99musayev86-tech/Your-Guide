// Voice synthesis and recognition utilities for AI Tutor

class SpeechController {
  private synth: SpeechSynthesis | null = null;
  private currentUtterance: SpeechSynthesisUtterance | null = null;
  private isSpeakingState = false;

  constructor() {
    if (typeof window !== "undefined" && "speechSynthesis" in window) {
      this.synth = window.speechSynthesis;
    }
  }

  public isAvailable(): boolean {
    return !!this.synth;
  }

  public speak(
    text: string,
    lang = "ru-RU",
    onEnd?: () => void,
    onError?: () => void
  ) {
    if (!this.synth) return;

    this.stop();

    // Clean markdown symbols for cleaner speech
    const cleanText = text
      .replace(/[*#`_~\[\]()><]/g, " ")
      .replace(/(\$\$|\$)/g, " ")
      .replace(/https?:\/\/\S+/g, " ")
      .slice(0, 1000); // safety length for web speech

    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.lang = lang;
    utterance.rate = 1.0;
    utterance.pitch = 1.05;

    // Pick appropriate voice if available
    const voices = this.synth.getVoices();
    const voice = voices.find(
      (v) => v.lang.startsWith(lang.slice(0, 2)) && (v.name.includes("Google") || v.name.includes("Natural") || v.name.includes("Yuri") || v.name.includes("Milena"))
    ) || voices.find((v) => v.lang.startsWith(lang.slice(0, 2)));

    if (voice) {
      utterance.voice = voice;
    }

    utterance.onstart = () => {
      this.isSpeakingState = true;
    };

    utterance.onend = () => {
      this.isSpeakingState = false;
      if (onEnd) onEnd();
    };

    utterance.onerror = () => {
      this.isSpeakingState = false;
      if (onError) onError();
    };

    this.currentUtterance = utterance;
    this.synth.speak(utterance);
  }

  public stop() {
    if (this.synth) {
      this.synth.cancel();
      this.isSpeakingState = false;
    }
  }

  public isSpeaking(): boolean {
    return this.synth ? this.synth.speaking || this.isSpeakingState : false;
  }
}

export const speech = new SpeechController();

// Voice recognition helper
export function createSpeechRecognizer(
  onResult: (text: string) => void,
  onError?: (err: any) => void
) {
  if (typeof window === "undefined") return null;

  const SpeechRecognition =
    (window as any).SpeechRecognition ||
    (window as any).webkitSpeechRecognition;

  if (!SpeechRecognition) return null;

  try {
    const recognition = new SpeechRecognition();
    recognition.lang = "ru-RU";
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.onresult = (event: any) => {
      const transcript = event.results[0][0].transcript;
      onResult(transcript);
    };

    recognition.onerror = (event: any) => {
      if (onError) onError(event);
    };

    return recognition;
  } catch (e) {
    console.warn("Speech recognition not supported:", e);
    return null;
  }
}
