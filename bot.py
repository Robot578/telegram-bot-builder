import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# ===== БЕРЕМ КЛЮЧИ ИЗ ПЕРЕМЕННЫХ ОКРУЖЕНИЯ =====
TOKEN = "8659343011:AAF3sk3LVUqbC41bFlhh9ccWJE90R6StvbE"
DEEPSEEK_KEY = "sk-0abd7a38a00b4b28b34449ec80be378e"
# ================================================

DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"

async def start(update, context):
    await update.message.reply_text(
        "👋 Привет! Я создаю ботов по описанию.\n\n"
        "Просто напиши, какого бота ты хочешь, например:\n"
        "'Сделай бота, который присылает анекдоты каждый час'\n\n"
        "Я сгенерирую код, и ты сможешь запустить бота за 5 минут!"
    )

async def generate_bot(update, context):
    user_text = update.message.text
    
    await update.message.reply_text("⏳ Генерирую код... Подожди 5-10 секунд.")
    
    prompt = f"""
    Напиши код для Telegram-бота на Python с библиотекой python-telegram-bot.
    
    Описание бота: {user_text}
    
    Требования:
    - Команда /start с приветствием
    - Реализовать логику из описания
    - Код должен работать сразу
    - Добавь комментарии на русском
    
    Отправь только код, без лишнего текста.
    """
    
    try:
        headers = {"Authorization": f"Bearer {DEEPSEEK_KEY}"}
        data = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 2000
        }
        
        response = requests.post(DEEPSEEK_URL, headers=headers, json=data, timeout=25)
        result = response.json()
        code = result["choices"][0]["message"]["content"]
        
        if "```python" in code:
            code = code.split("```python")[1].split("```")[0]
        elif "```" in code:
            code = code.split("```")[1].split("```")[0]
        
        await update.message.reply_text(
            f"✅ Готово!\n\n"
            f"```python\n{code}\n```\n\n"
            f"📌 КАК ЗАПУСТИТЬ (бесплатно):\n"
            f"1. Зайди на replit.com\n"
            f"2. Создай новый проект на Python\n"
            f"3. Вставь этот код\n"
            f"4. Напиши @BotFather, создай бота и получи токен\n"
            f"5. Вставь токен в код (вместо 'ТВОЙ_ТОКЕН')\n"
            f"6. Нажми Run — бот заработает!",
            parse_mode="Markdown"
        )
        
    except Exception as e:
        await update.message.reply_text(
            f"❌ Ошибка: {str(e)}\n\n"
            "Попробуй написать короче или перефразируй запрос."
        )

def main():
    if not TOKEN or not DEEPSEEK_KEY:
        print("❌ Ошибка: Не заданы переменные окружения TOKEN и DEEPSEEK_KEY")
        return
    
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_bot))
    
    print("🤖 Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
