import io # Добавьте этот импорт в начало файла

# ... (код выше) ...

@dp.message_handler(content_types=['photo'])
async def handle_photo(message: types.Message):
    await bot.send_chat_action(message.chat.id, action="typing")
    
    # 1. Получаем файл фото
    photo = message.photo[-1] # Берем фото самого лучшего качества
    file_info = await bot.get_file(photo.file_id)
    downloaded_file = await bot.download_file(file_info.file_path)
    
    # 2. Превращаем фото в формат, понятный Gemini
    image_bytes = downloaded_file.read()
    image_data = {
        "mime_type": "image/jpeg",
        "data": image_bytes
    }
    
    # 3. Отправляем в Gemini запрос с описанием
    response = model.generate_content([
        "Расскажи историю этого места, его название и интересные факты.", 
        image_data
    ])
    
    await message.answer(response.text)
  aiogram==2.25.1
google-generativeai
Pillow  # Эта библиотека нужна для обработки изображений
AQ.Ab8RN6KsSn51T1Ve5s_ikreAYfSoml7kIFwK8DawqVmdSBYReA
