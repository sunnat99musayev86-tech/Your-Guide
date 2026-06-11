import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from gtts import gTTS
import google.generativeai as genai

# 1. ВСТАВЬТЕ СЮДА ВАШ ТОКЕН TELEGRAM
API_TOKEN = '8980910424:AAFRqavkI1LjR2-7Q7el29UXBJdhsB9HppI'

# 2. ВСТАВЬТЕ СЮДА ВАШ API KEY GOOGLE GEMINI
genai.configure(api_key='AQ.Ab8RN6KsSn51T1Ve5s_ikreAYfSoml7kIFwK8DawqVmdSBYReA')

model = genai.GenerativeModel('gemini-pro')

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Меню
def get_main_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("📍 Где я?", callback_data="loc_info"),
        InlineKeyboardButton("📸 Фото-перевод", callback_data="photo_trans"),
        InlineKeyboardButton("🌍 Переводчик", callback_data="translate"),
        InlineKeyboardButton("📤 Поделиться", callback_data="share")
    )
    return markup

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(
        "✨ *Привет, дорогой путешественник!* ✨\n\n"
        "Я твой личный гид. Спрашивай меня о чем угодно, присылай локацию или фото!",
        reply_markup=get_main_menu(), parse_mode="Markdown"
    )

@dp.message_handler(content_types=['location'])
async def handle_location(message: types.Message):
    lat, lon = message.location.latitude, message.location.longitude
    prompt = f"Пользователь находится на {lat}, {lon}. Расскажи очень мягко, с юмором, историю этого места."
    response = model.generate_content(prompt)
    
    tts = gTTS(text=response.text, lang='ru')
    tts.save("response.ogg")
    with open("response.ogg", "rb") as voice:
        await message.reply_voice(voice)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
  
