from flask import Blueprint, request, jsonify
import logging
import os
from dotenv import load_dotenv
from flask_cors import CORS
from openai import OpenAI

# Загрузка переменных окружения
load_dotenv()

# Создание Blueprint
main = Blueprint('main', __name__)

# Настройка CORS для Blueprint
CORS(main)

# Получение API ключа из переменных окружения
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")

# Чтение системного промпта из файла
file_path = os.path.join(os.path.dirname(__file__), 'system_prompt.json')
with open(file_path, 'r', encoding='utf-8') as file:
    system_content = file.read()

# Инициализация клиента OpenAI
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=openrouter_api_key,
)

@main.route('/api/query', methods=['POST'])
def query_deepseek():
    try:
        data = request.json
        user_input = data.get('input')

        if not openrouter_api_key:
            logging.error("API ключ не найден.")
            return jsonify({'error': 'Ошибка системы. Попробуйте позже.'}), 500

        if not user_input:
            logging.error("Пустой запрос от пользователя.")
            return jsonify({'error': 'Запрос не может быть пустым.'}), 400

        # Логирование system_content и user_input
        logging.info(f"Содержимое system_content: {system_content}")
        logging.info(f"Запрос от пользователя: {user_input}")

        # Отправка запроса на сервер OpenRouter
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "<YOUR_SITE_URL>",  # Укажите URL вашего сайта
                "X-Title": "<YOUR_SITE_NAME>",  # Укажите название вашего сайта
            },
            extra_body={},
            model="google/gemini-2.0-flash-lite-preview-02-05:free",
            messages=[
                {
                    "role": "system",
                    "content": system_content,
                },
                {
                    "role": "user",
                    "content": user_input,
                }
            ]
        )

        logging.info(f"Ответ от сервера: {completion.choices[0].message.content}")

        return jsonify({'response': completion.choices[0].message.content})

    except Exception as e:
        logging.error(f"Ошибка API: {e}")
        return jsonify({'error': str(e)}), 500
