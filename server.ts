import express from "express";
import path from "path";
import dotenv from "dotenv";
import { GoogleGenAI, Type } from "@google/genai";

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json({ limit: "25mb" }));

// Initialize Google GenAI client
const apiKey = process.env.GEMINI_API_KEY;
const ai = new GoogleGenAI({
  apiKey: apiKey || "",
  httpOptions: {
    headers: {
      "User-Agent": "aistudio-build",
    },
  },
});

const DEFAULT_MODEL = "gemini-3.8-flash";

// System instructions builder based on role & mode
function buildTutorSystemPrompt(params: {
  subject?: string;
  topic?: string;
  level?: string;
  mode?: string;
  tone?: string;
}) {
  const {
    subject = "Математика",
    topic = "Общие вопросы",
    level = "Школа (9-11 класс / ОГЭ / ЕГЭ)",
    mode = "socratic",
    tone = "encouraging",
  } = params;

  let toneInstruction = "Будь доброжелательным, поддерживающим и чутким наставником. Хвали за успехи, мотивируй и мягко направляй при ошибках.";
  if (tone === "strict") {
    toneInstruction = "Будь академичным, строгим и точным преподавателем. Требуй строгих формулировок, точности терминов и аккуратных выкладок.";
  } else if (tone === "friendly_peer") {
    toneInstruction = "Общайся как крутой старший друг-студент или одноклассник: легко, живо, с понятными жизненными метафорами, легким юмором и без занудства.";
  } else if (tone === "olympiad") {
    toneInstruction = "Будь олимпиадным тренером: стимулируй нестандартное мышление, поиск изящных и красивых методов решения, учи видеть скрытые свойства.";
  }

  let modeInstruction = "";
  if (mode === "socratic") {
    modeInstruction = `
РЕЖИМ: СОКРАТОВСКИЙ МЕТОД (ДИАЛОГОВЫЙ ТЬЮТОР).
- Твоя главная цель — НЕ давать готовый ответ сразу!
- Задавай наводящие вопросы, разбивай сложную мысль на простые логические шаги.
- Если ученик даёт верный шаг, подтверди и задай следующий вопрос.
- Если ученик ошибается, не говори просто "неправильно", а предложи проверить конкретное место (например: "Посмотри внимательно на знак минуса перед скобками...").
- Используй аналогии. Только если ученик совсем застрял после нескольких подсказок, покажи один шаг и попроси сделать следующий самостоятельно.
`;
  } else if (mode === "expert") {
    modeInstruction = `
РЕЖИМ: ЭКСПЕРТНЫЙ ПОШАГОВЫЙ РАЗБОР.
- Дай кристально чистое, глубокое и последовательное решение или объяснение.
- Выдели: 1) Дано / Что требуется, 2) Необходимые формулы / правила, 3) Пошаговый ход мысли с обоснованием каждого действия, 4) Частые ошибки учеников в таких заданиях, 5) Проверка ответа.
`;
  } else if (mode === "exam_prep") {
    modeInstruction = `
РЕЖИМ: ПОДГОТОВКА К ЭКЗАМЕНАМ (ЕГЭ, ОГЭ, Сессия, Экзамен).
- Фокусируйся на структуре экзаменационных заданий, критериях оценивания (за что снимают баллы), правильном оформлении решений и ловушках составителей.
- Указывай лайфхаки распределения времени и самопроверки.
`;
  } else if (mode === "language_practice") {
    modeInstruction = `
РЕЖИМ: ЯЗЫКОВАЯ ПРАКТИКА (ИНОСТРАННЫЙ ЯЗЫК).
- Если изучается английский или другой язык, веди диалог преимущественно на изучаемом языке (с пояснениями на русском при необходимости).
- Корректируй грамматику и лексику ученика: мягко исправляй ошибки, предлагай более естественные идиомы (natural phrasing), объясняй контекст употребления.
`;
  }

  return `Ты — интерактивный персональный ИИ Репетитор высшей квалификации.
Предмет: ${subject}
Текущая тема: ${topic}
Уровень ученика: ${level}

${toneInstruction}
${modeInstruction}

Оформление ответов:
- Форматируй математические формулы и выкладки красиво с помощью Markdown (используй четкие математические символы, степени, дроби или KaTeX стиль: например, x² + y² = r²).
- Используй списки, выделения полужирным для ключевых терминов и читаемые абзацы.
- Текст должен быть приятным для чтения, без сухой стены текста.
- Всегда отвечай на русском языке (если только предмет не требует общения на иностранном).
`;
}

// 1. Chat endpoint with streaming (SSE)
app.post("/api/tutor/chat", async (req, res) => {
  try {
    const { messages, subject, topic, level, mode, tone } = req.body;

    if (!messages || !Array.isArray(messages) || messages.length === 0) {
      return res.status(400).json({ error: "Массив сообщений обязателен" });
    }

    const systemInstruction = buildTutorSystemPrompt({ subject, topic, level, mode, tone });

    // Format contents for Gemini
    const contents = messages.map((m: any) => {
      const parts: any[] = [];

      if (m.imageBase64) {
        // Strip data:image/...;base64, prefix if present
        let base64Data = m.imageBase64;
        let mimeType = "image/jpeg";
        const match = base64Data.match(/^data:([^;]+);base64,(.+)$/);
        if (match) {
          mimeType = match[1];
          base64Data = match[2];
        }
        parts.push({
          inlineData: {
            mimeType,
            data: base64Data,
          },
        });
      }

      if (m.text) {
        parts.push({ text: m.text });
      }

      return {
        role: m.role === "user" ? "user" : "model",
        parts,
      };
    });

    // Set SSE headers
    res.setHeader("Content-Type", "text/event-stream");
    res.setHeader("Cache-Control", "no-cache");
    res.setHeader("Connection", "keep-alive");

    const streamResponse = await ai.models.generateContentStream({
      model: DEFAULT_MODEL,
      contents,
      config: {
        systemInstruction,
      },
    });

    for await (const chunk of streamResponse) {
      if (chunk.text) {
        res.write(`data: ${JSON.stringify({ text: chunk.text })}\n\n`);
      }
    }

    res.write("data: [DONE]\n\n");
    res.end();
  } catch (error: any) {
    console.error("Error in /api/tutor/chat:", error);
    if (!res.headersSent) {
      res.status(500).json({
        error: error.message || "Ошибка при генерации ответа репетитора",
      });
    } else {
      res.write(`data: ${JSON.stringify({ error: error.message || "Ошибка стриминга" })}\n\n`);
      res.end();
    }
  }
});

// 2. Step-by-Step Solver endpoint (photo or text task)
app.post("/api/tutor/solve", async (req, res) => {
  try {
    const { text, imageBase64, subject, topic, level } = req.body;

    if (!text && !imageBase64) {
      return res.status(400).json({ error: "Необходимо передать текст задания или изображение" });
    }

    const parts: any[] = [];
    if (imageBase64) {
      let base64Data = imageBase64;
      let mimeType = "image/jpeg";
      const match = base64Data.match(/^data:([^;]+);base64,(.+)$/);
      if (match) {
        mimeType = match[1];
        base64Data = match[2];
      }
      parts.push({
        inlineData: {
          mimeType,
          data: base64Data,
        },
      });
    }

    const promptText = `
Пожалуйста, реши и подробно разбери следующую задачу/вопрос:
"${text || "Разбери задачу с прикрепленного изображения"}"

Предмет: ${subject || "Естественно-научный/Математика"}
Тема: ${topic || "Общая"}
Уровень: ${level || "Стандартный"}

Дай структурированный ответ с разделами:
1. **Условие и формулировка** (краткая выжимка того, что дано и что найти)
2. **Теория и формулы** (какие правила, законы, теоремы или формулы понадобятся)
3. **Пошаговое решение** (подробные математические/логические шаги с пояснением «почему»)
4. **Итоговый ответ** (четко выделенный результат)
5. **Частая ловушка / ошибка** (на чем обычно сыплются ученики в таких задачах)
6. **Аналогичное мини-задание для самопроверки** (чтобы ученик мог закрепить материал)
`;
    parts.push({ text: promptText });

    const response = await ai.models.generateContent({
      model: DEFAULT_MODEL,
      contents: { parts },
      config: {
        systemInstruction: "Ты — высококлассный преподаватель и эксперт по решению задач. Твои решения образцово понятные, логичные, без пропусков важных промежуточных вычислений.",
      },
    });

    res.json({ result: response.text });
  } catch (error: any) {
    console.error("Error in /api/tutor/solve:", error);
    res.status(500).json({ error: error.message || "Ошибка решения задачи" });
  }
});

// 3. Quiz Generation endpoint (Structured JSON)
app.post("/api/tutor/quiz", async (req, res) => {
  try {
    const { subject, topic, level, count = 5 } = req.body;

    const prompt = `Сгенерируй интерактивный проверочный тест по предмету "${subject}", тема: "${topic}", уровень сложности: "${level}". Количество вопросов: ${count}.
Каждый вопрос должен иметь ровно 4 варианта ответа, правильный индекс (0-3), понятное объяснение правильного ответа и короткую подсказку.`;

    const response = await ai.models.generateContent({
      model: DEFAULT_MODEL,
      contents: prompt,
      config: {
        responseMimeType: "application/json",
        responseSchema: {
          type: Type.ARRAY,
          items: {
            type: Type.OBJECT,
            properties: {
              question: {
                type: Type.STRING,
                description: "Текст вопроса или задачи",
              },
              options: {
                type: Type.ARRAY,
                items: { type: Type.STRING },
                description: "4 варианта ответа",
              },
              correctIndex: {
                type: Type.INTEGER,
                description: "Индекс верного ответа от 0 до 3",
              },
              explanation: {
                type: Type.STRING,
                description: "Подробное объяснение, почему этот ответ верный",
              },
              hint: {
                type: Type.STRING,
                description: "Наводящая подсказка для ученика",
              },
              difficulty: {
                type: Type.STRING,
                description: "Легкий, Средний или Сложный",
              },
            },
            required: ["question", "options", "correctIndex", "explanation", "hint", "difficulty"],
          },
        },
      },
    });

    const parsed = JSON.parse(response.text || "[]");
    res.json({ questions: parsed });
  } catch (error: any) {
    console.error("Error in /api/tutor/quiz:", error);
    res.status(500).json({ error: error.message || "Ошибка генерации теста" });
  }
});

// 4. Flashcards Deck generation endpoint (Structured JSON)
app.post("/api/tutor/flashcards", async (req, res) => {
  try {
    const { subject, topic, level, count = 8 } = req.body;

    const prompt = `Создай колоду карточек для запоминания (флеш-карточки / Anki) по теме "${topic}" (предмет: ${subject}, уровень: ${level}). Количество: ${count}.
Каждая карточка должна иметь чёткую лицевую сторону (термин, вопрос или формула), оборотную сторону (точное определение, ответ, пример) и мнемонику/ассоциацию для быстрого запоминания.`;

    const response = await ai.models.generateContent({
      model: DEFAULT_MODEL,
      contents: prompt,
      config: {
        responseMimeType: "application/json",
        responseSchema: {
          type: Type.ARRAY,
          items: {
            type: Type.OBJECT,
            properties: {
              front: {
                type: Type.STRING,
                description: "Лицевая сторона: термин, формула или вопрос",
              },
              back: {
                type: Type.STRING,
                description: "Оборотная сторона: развернутый ответ, суть правила, пример применения",
              },
              mnemonic: {
                type: Type.STRING,
                description: "Мнемоническое правило, метафора или ассоциация для запоминания",
              },
              category: {
                type: Type.STRING,
                description: "Подкатегория или тип карточки (Формула, Термин, Правило, Исключение)",
              },
            },
            required: ["front", "back", "mnemonic", "category"],
          },
        },
      },
    });

    const parsed = JSON.parse(response.text || "[]");
    res.json({ flashcards: parsed });
  } catch (error: any) {
    console.error("Error in /api/tutor/flashcards:", error);
    res.status(500).json({ error: error.message || "Ошибка создания карточек" });
  }
});

// 5. Study Plan & Roadmap generation endpoint (Structured JSON)
app.post("/api/tutor/plan", async (req, res) => {
  try {
    const { subject, targetGoal, availableTime, currentLevel } = req.body;

    const prompt = `Составь детальный индивидуальный учебный план для ученика.
Предмет: ${subject}
Цель: ${targetGoal || "Освоить основы и сдать экзамен"}
Текущий уровень: ${currentLevel || "Начальный"}
Доступное время: ${availableTime || "4 недели по 3 часа в неделю"}`;

    const response = await ai.models.generateContent({
      model: DEFAULT_MODEL,
      contents: prompt,
      config: {
        responseMimeType: "application/json",
        responseSchema: {
          type: Type.OBJECT,
          properties: {
            title: { type: Type.STRING, description: "Название плана" },
            estimatedTotalHours: { type: Type.INTEGER, description: "Всего часов" },
            overview: { type: Type.STRING, description: "Краткий обзор стратегии обучения" },
            modules: {
              type: Type.ARRAY,
              items: {
                type: Type.OBJECT,
                properties: {
                  weekNumber: { type: Type.INTEGER },
                  title: { type: Type.STRING },
                  objectives: { type: Type.ARRAY, items: { type: Type.STRING } },
                  practiceTask: { type: Type.STRING },
                  selfCheckQuestion: { type: Type.STRING },
                },
                required: ["weekNumber", "title", "objectives", "practiceTask", "selfCheckQuestion"],
              },
            },
            tips: { type: Type.ARRAY, items: { type: Type.STRING } },
          },
          required: ["title", "estimatedTotalHours", "overview", "modules", "tips"],
        },
      },
    });

    const parsed = JSON.parse(response.text || "{}");
    res.json({ plan: parsed });
  } catch (error: any) {
    console.error("Error in /api/tutor/plan:", error);
    res.status(500).json({ error: error.message || "Ошибка генерации плана" });
  }
});

// 6. Explain concept in 3 levels endpoint
app.post("/api/tutor/explain", async (req, res) => {
  try {
    const { concept, subject } = req.body;

    if (!concept) {
      return res.status(400).json({ error: "Укажите понятие для объяснения" });
    }

    const prompt = `Объясни понятие/явление/теорему: "${concept}" (Предмет: ${subject || "Общий"}).
Разбей объяснение на 3 уровня:
1. simple: Объяснение "как для 5-летнего" (яркая житейская аналогия или метафора)
2. academic: Строгое научное определение, ключевые свойства, формулы и термины
3. realLife: Где и как это применяется в реальном мире, технологиях или повседневной жизни
4. quickQuestion: Быстрый проверочный вопрос для ученика на понимание сути`;

    const response = await ai.models.generateContent({
      model: DEFAULT_MODEL,
      contents: prompt,
      config: {
        responseMimeType: "application/json",
        responseSchema: {
          type: Type.OBJECT,
          properties: {
            concept: { type: Type.STRING },
            simple: { type: Type.STRING },
            academic: { type: Type.STRING },
            realLife: { type: Type.STRING },
            quickQuestion: { type: Type.STRING },
          },
          required: ["concept", "simple", "academic", "realLife", "quickQuestion"],
        },
      },
    });

    const parsed = JSON.parse(response.text || "{}");
    res.json({ explanation: parsed });
  } catch (error: any) {
    console.error("Error in /api/tutor/explain:", error);
    res.status(500).json({ error: error.message || "Ошибка объяснения концепта" });
  }
});

// Vite middleware in dev or static serving in prod
async function startServer() {
  if (process.env.NODE_ENV !== "production") {
    const { createServer: createViteServer } = await import("vite");
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: "spa",
    });
    app.use(vite.middlewares);
  } else {
    const distPath = path.resolve(process.cwd(), "dist");
    app.use(express.static(distPath));
    app.get("*", (_req, res) => {
      res.sendFile(path.resolve(distPath, "index.html"));
    });
  }

  app.listen(PORT, () => {
    console.log(`AI Tutor Server running on port ${PORT}`);
  });
}

startServer();
