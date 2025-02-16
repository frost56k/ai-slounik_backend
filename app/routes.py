from flask import Blueprint, request, jsonify
import logging
import os
from dotenv import load_dotenv
from openai import OpenAI

# Загрузка переменных окружения
load_dotenv()

# Создание Blueprint
main = Blueprint('main', __name__)

# Получение API ключа из переменных окружения
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")

# Путь к системному промпту
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, 'system_prompt.json')

try:
    with open(file_path, 'r', encoding='utf-8') as file:
        system_content = file.read()
except FileNotFoundError:
    logging.error("Файл system_prompt.json не найден!")
    system_content = ""

# Инициализация клиента OpenAI
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=openrouter_api_key,
) if openrouter_api_key else None

@main.route('/api/query', methods=['POST'])
def query_deepseek():
    try:
        if not client:
            logging.error("OpenAI клиент не инициализирован")
            return jsonify({'error': 'Ошибка конфигурации сервера'}), 500

        logging.info("Запрос получен на /api/query")
        data = request.get_json()
        
        if not data:
            logging.error("Отсутствует тело запроса")
            return jsonify({'error': 'Неверный формат запроса'}), 400
            
        user_input = data.get('input')

        if not user_input or not user_input.strip():
            logging.error("Пустой запрос от пользователя")
            return jsonify({'error': 'Запрос не может быть пустым'}), 400

        logging.debug(f"Обработка запроса: {user_input[:50]}...")

        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "https://ai-slounik.andchar.of.by",
                "X-Title": "AI Slounik",
            },
            model="google/gemini-2.0-flash-lite-preview-02-05:free",
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": user_input}
            ]
        )

        if not completion.choices[0].message.content:
            logging.error("Пустой ответ от API")
            return jsonify({'error': 'Ошибка обработки запроса'}), 500

        logging.info("Успешный ответ от API")
        return jsonify({
            'response': completion.choices[0].message.content,
            'model': completion.model
        })

    except Exception as e:
        logging.error(f"Критическая ошибка: {str(e)}", exc_info=True)
        return jsonify({'error': 'Внутренняя ошибка сервера'}), 500
