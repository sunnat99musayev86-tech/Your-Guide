Please finalize the complete App.js code for the "AI Voice Tutor" with all features fully integrated:
1. Interactive UI: Make every top element (Balance badge with paywall modal, Profile avatar, Settings, Notifications), scenario card (Job Interview, Airport Customs, Ordering Coffee), and bottom tag (Figma, Team template) fully clickable and interactive.
2. Human-like AI & Auto-Language Detection: Update the Gemini API system prompt so the AI acts as a warm, empathetic human tutor who automatically detects the user's spoken language and replies naturally in the exact same language (concise 1-3 sentences).
3. Speech Integration: Process audio via Groq Whisper API, send to Gemini, and dynamically set `expo-speech` language options to match the response language.
4. Monetization & Balance: Deduct balance during voice sessions and open the paywall modal ($1.99 / 60m, $4.99 / 300m, 'Watch Ad for +5 mins') when clicking the balance badge.
Ensure all imports, styles, and safe environment variable handling (.env hidden from GitHub) are clean and ready for final commit.
