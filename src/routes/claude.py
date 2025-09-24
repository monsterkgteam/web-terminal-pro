import os
from flask import Blueprint, request, jsonify
from anthropic import Anthropic

claude_bp = Blueprint('claude', __name__)

# Инициализация клиента Claude (API ключ должен быть установлен в переменной окружения)
def get_claude_client():
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        return None
    return Anthropic(api_key=api_key)

@claude_bp.route('/chat', methods=['POST'])
def chat_with_claude():
    """Отправляет сообщение Claude и возвращает ответ"""
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'Сообщение не предоставлено'}), 400
            
        client = get_claude_client()
        if not client:
            return jsonify({'error': 'API ключ Claude не настроен. Установите ANTHROPIC_API_KEY в переменные окружения.'}), 500
            
        message = data['message']
        model = data.get('model', 'claude-3-sonnet-20240229')
        max_tokens = data.get('max_tokens', 1000)
        
        # Отправляем запрос к Claude
        response = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            messages=[
                {
                    "role": "user",
                    "content": message
                }
            ]
        )
        
        return jsonify({
            'response': response.content[0].text,
            'model': model,
            'usage': {
                'input_tokens': response.usage.input_tokens,
                'output_tokens': response.usage.output_tokens
            }
        })
        
    except Exception as e:
        return jsonify({'error': f'Ошибка при обращении к Claude: {str(e)}'}), 500

@claude_bp.route('/models', methods=['GET'])
def get_available_models():
    """Возвращает список доступных моделей Claude"""
    models = [
        {
            'id': 'claude-3-opus-20240229',
            'name': 'Claude 3 Opus',
            'description': 'Самая мощная модель для сложных задач'
        },
        {
            'id': 'claude-3-sonnet-20240229',
            'name': 'Claude 3 Sonnet',
            'description': 'Баланс производительности и скорости'
        },
        {
            'id': 'claude-3-haiku-20240307',
            'name': 'Claude 3 Haiku',
            'description': 'Быстрая модель для простых задач'
        }
    ]
    return jsonify({'models': models})

@claude_bp.route('/status', methods=['GET'])
def claude_status():
    """Проверяет статус подключения к Claude API"""
    try:
        client = get_claude_client()
        if not client:
            return jsonify({
                'status': 'not_configured',
                'message': 'API ключ Claude не настроен'
            })
            
        # Простой тестовый запрос
        response = client.messages.create(
            model='claude-3-haiku-20240307',
            max_tokens=10,
            messages=[{"role": "user", "content": "Hi"}]
        )
        
        return jsonify({
            'status': 'connected',
            'message': 'Claude API работает корректно'
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Ошибка подключения к Claude: {str(e)}'
        }), 500
