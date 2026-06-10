from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import google.generativeai as genai

# Вставьте ваши токены
TELEGRAM_TOKEN = 'ВАШ_TELEGRAM_TOKEN'
GOOGLE_API_KEY = 'ВАШ_GEMINI_API_KEY'

# Настройка Gemini
genai.configure(AQ.Ab8RN6KsSn51T1Ve5s_ikreAYfSoml7kIFwK8DawqVmdSBYReA)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = Bot(8980910424:AAFRqavkI1LjR2-7Q7el29UXBJdhsB9HppI)
dp = Dispatcher(bot)

# Кнопки меню остаются прежними
def get_main_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(KeyboardButton("🎙 Голосовой помощник"), KeyboardButton("📷 Фото-сканер"))
    keyboard.add(KeyboardButton("📍 Где я?"), KeyboardButton("🌍 О городе/месте"))
    return keyboard

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Салом! Я ваш глобальный ИИ-гид на базе Gemini. Что вас интересует?", reply_markup=get_main_menu())

@dp.message_handler(content_types=['text', 'photo', 'voice', 'location'])
async def handle_everything(message: types.Message):
    await bot.send_chat_action(message.chat.id, action="typing")
    
    # Формируем промпт
    if message.location:
        prompt = f"Пользователь здесь: {message.location.latitude}, {message.location.longitude}. Расскажи, что рядом интересного."
    elif message.photo:
        # Для фото в Gemini нужно передавать файл, это требует чуть другой логики
        prompt = "Расскажи историю этого места по фото."
    elif message.voice:
        prompt = "Пользователь прислал голосовое. Ответь на его вопрос."
    else:
        prompt = message.text

    # Запрос к Gemini
    response = model.generate_content(prompt)
    await message.answer(response.text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    
