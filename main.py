import React, { useState, useEffect } from 'react';
import { 
  StyleSheet, 
  Text, 
  View, 
  TouchableOpacity, 
  SafeAreaView, 
  ScrollView, 
  ActivityIndicator,
  StatusBar
} from 'react-native';
import * as Speech from 'expo-speech';

// --- НАСТРОЙКИ API КЛЮЧЕЙ ---
const GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"; // Вставьте бесплатный ключ Google AI Studio
const GROQ_API_KEY = "YOUR_GROQ_API_KEY";     // Вставьте бесплатный ключ GroqCloud

export default function App() {
  const [balance, setBalance] = useState(120); // Баланс минут
  const [isListening, setIsListening] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [userText, setUserText] = useState("");
  const [aiResponse, setAiResponse] = useState("Hello! Choose a scenario above or tap the mic to start speaking.");
  const [selectedScenario, setSelectedScenario] = useState("Free Talk");

  // Озвучка ответа ИИ через встроенный движок телефона
  const speakResponse = (text) => {
    Speech.stop();
    Speech.speak(text, {
      language: 'en-US',
      pitch: 1.0,
      rate: 0.9,
    });
  };

  // Вызов Google Gemini API (Бесплатный Мозг)
  const callGeminiAI = async (userPrompt) => {
    setIsLoading(true);
    try {
      const response = await fetch(
        `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${GEMINI_API_KEY}`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            contents: [{
              parts: [{
                text: `You are a supportive, friendly AI Voice Tutor for language practice in scenario: "${selectedScenario}". 
                       Keep answers concise (1-3 sentences) suitable for spoken speech. 
                       If the user made a grammar error, gently correct it at the end in brackets. 
                       User said: "${userPrompt}"`
              }]
            }]
          })
        }
      );
      
      const data = await response.json();
      const reply = data.candidates?.[0]?.content?.parts?.[0]?.text || "Sorry, I didn't catch that. Could you repeat?";
      
      setAiResponse(reply);
      speakResponse(reply);
    } catch (error) {
      console.error("Gemini API Error:", error);
      setAiResponse("Connection error. Please check your API key.");
    } finally {
      setIsLoading(false);
    }
  };

  // Эмуляция/запуск записи голоса
  const handleMicPress = () => {
    if (balance <= 0) {
      alert("No minutes left! Please top up.");
      return;
    }

    if (isListening) {
      setIsListening(false);
      // В реальной сборке здесь аудиофайл отправляется в Groq Whisper API
      // Симуляция распознанной речи для теста:
      const simulatedSpeech = "Hello, I want to order a coffee please.";
      setUserText(simulatedSpeech);
      callGeminiAI(simulatedSpeech);
      setBalance(prev => Math.max(0, prev - 1));
    } else {
      setIsListening(true);
      setUserText("Listening...");
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor="#0F172A" />
      
      {/* 1. Header (Баланс минут и Имя) */}
      <View style={styles.header}>
        <View style={styles.balanceBadge}>
          <Text style={styles.balanceText}>💎 {balance} mins left</Text>
        </View>
        <Text style={styles.titleText}>AI Voice Tutor</Text>
      </View>

      <ScrollView contentContainerStyle={styles.content}>
        {/* 2. Выбор Сценариев */}
        <Text style={styles.sectionTitle}>Select Scenario</Text>
        <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.scenarioList}>
          {['Free Talk', 'Job Interview', 'Airport Customs', 'Coffee Shop'].map((item) => (
            <TouchableOpacity 
              key={item} 
              style={[styles.scenarioCard, selectedScenario === item && styles.selectedCard]}
              onPress={() => setSelectedScenario(item)}
            >
              <Text style={styles.scenarioText}>{item}</Text>
            </TouchableOpacity>
          ))}
        </ScrollView>

        {/* 3. Диалоговый экран (Ответ ИИ и Голос) */}
        <View style={styles.chatBox}>
          <Text style={styles.aiLabel}>Tutor Response ({selectedScenario}):</Text>
          <Text style={styles.aiText}>{aiResponse}</Text>
          {userText !== "" && (
            <Text style={styles.userText}>You: {userText}</Text>
          )}
        </View>

        {/* 4. Центральная кнопка микрофона */}
        <View style={styles.micContainer}>
          <TouchableOpacity 
            style={[styles.micButton, isListening && styles.micActive]} 
            onPress={handleMicPress}
            disabled={isLoading}
          >
            {isLoading ? (
              <ActivityIndicator color="#FFF" size="large" />
            ) : (
              <Text style={styles.micIcon}>{isListening ? "⏹️" : "🎙️"}</Text>
            )}
          </TouchableOpacity>
          <Text style={styles.micHint}>
            {isListening ? "Tap to Stop & Send" : "Tap to Speak"}
          </Text>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

// --- СТИЛИ ДИЗАЙНА (Deep Violet & Dark Slate) ---
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0F172A', // Dark background
  },
  header: {
    flexDirection: 'row',
    justify: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingVertical: 15,
  },
  balanceBadge: {
    backgroundColor: '#1E293B',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 20,
    borderWidth: 1,
    borderColor: '#7C3AED',
  },
  balanceText: {
    color: '#F8FAFC',
    fontWeight: '600',
    fontSize: 14,
  },
  titleText: {
    color: '#FFF',
    fontSize: 18,
    fontWeight: 'bold',
  },
  content: {
    paddingHorizontal: 20,
    paddingBottom: 40,
  },
  sectionTitle: {
    color: '#94A3B8',
    fontSize: 14,
    marginBottom: 10,
    marginTop: 10,
  },
  scenarioList: {
    flexDirection: 'row',
    marginBottom: 20,
  },
  scenarioCard: {
    backgroundColor: '#1E293B',
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderRadius: 12,
    marginRight: 10,
  },
  selectedCard: {
    backgroundColor: '#7C3AED',
  },
  scenarioText: {
    color: '#FFF',
    fontWeight: '500',
  },
  chatBox: {
    backgroundColor: '#1E293B',
    padding: 20,
    borderRadius: 16,
    minHeight: 140,
    marginBottom: 30,
    borderColor: '#334155',
    borderWidth: 1,
  },
  aiLabel: {
    color: '#7C3AED',
    fontWeight: 'bold',
    marginBottom: 8,
  },
  aiText: {
    color: '#F8FAFC',
    fontSize: 16,
    lineHeight: 24,
  },
  userText: {
    color: '#94A3B8',
    fontSize: 14,
    marginTop: 12,
    fontStyle: 'italic',
  },
  micContainer: {
    alignItems: 'center',
    justify: 'center',
    marginTop: 10,
  },
  micButton: {
    width: 90,
    height: 90,
    borderRadius: 45,
    backgroundColor: '#7C3AED',
    alignItems: 'center',
    justify: 'center',
    elevation: 8,
    shadowColor: '#7C3AED',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.5,
    shadowRadius: 10,
  },
  micActive: {
    backgroundColor: '#EF4444',
  },
  micIcon: {
    fontSize: 36,
  },
  micHint: {
    color: '#94A3B8',
    marginTop: 12,
    fontSize: 14,
  }
});
