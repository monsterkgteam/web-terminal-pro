import os
import subprocess
import json
from flask import Blueprint, request, jsonify

gcloud_bp = Blueprint('gcloud', __name__)

def get_gcloud_path():
    """Возвращает путь к gcloud CLI"""
    return '/home/ubuntu/web-terminal-app/google-cloud-sdk/bin/gcloud'

def run_gcloud_command(command_args, timeout=30):
    """Выполняет команду gcloud и возвращает результат"""
    try:
        gcloud_path = get_gcloud_path()
        if not os.path.exists(gcloud_path):
            return {
                'success': False,
                'error': 'Google Cloud CLI не найден',
                'output': '',
                'stderr': ''
            }
        
        # Подготавливаем команду
        cmd = [gcloud_path] + command_args
        
        # Выполняем команду
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=dict(os.environ, PATH=os.environ.get('PATH', '') + ':/home/ubuntu/web-terminal-app/google-cloud-sdk/bin')
        )
        
        return {
            'success': result.returncode == 0,
            'returncode': result.returncode,
            'output': result.stdout,
            'stderr': result.stderr
        }
        
    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'error': f'Команда превысила лимит времени ({timeout}s)',
            'output': '',
            'stderr': ''
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'Ошибка выполнения команды: {str(e)}',
            'output': '',
            'stderr': ''
        }

@gcloud_bp.route('/version', methods=['GET'])
def gcloud_version():
    """Возвращает версию Google Cloud CLI"""
    result = run_gcloud_command(['version', '--format=json'])
    
    if result['success']:
        try:
            version_info = json.loads(result['output'])
            return jsonify({
                'status': 'success',
                'version': version_info
            })
        except json.JSONDecodeError:
            return jsonify({
                'status': 'success',
                'version': result['output'].strip()
            })
    else:
        return jsonify({
            'status': 'error',
            'error': result.get('error', result['stderr'])
        }), 500

@gcloud_bp.route('/auth/list', methods=['GET'])
def list_auth_accounts():
    """Возвращает список аутентифицированных аккаунтов"""
    result = run_gcloud_command(['auth', 'list', '--format=json'])
    
    if result['success']:
        try:
            accounts = json.loads(result['output'])
            return jsonify({
                'status': 'success',
                'accounts': accounts
            })
        except json.JSONDecodeError:
            return jsonify({
                'status': 'success',
                'accounts': [],
                'raw_output': result['output']
            })
    else:
        return jsonify({
            'status': 'error',
            'error': result.get('error', result['stderr'])
        }), 500

@gcloud_bp.route('/projects/list', methods=['GET'])
def list_projects():
    """Возвращает список проектов Google Cloud"""
    result = run_gcloud_command(['projects', 'list', '--format=json'])
    
    if result['success']:
        try:
            projects = json.loads(result['output'])
            return jsonify({
                'status': 'success',
                'projects': projects
            })
        except json.JSONDecodeError:
            return jsonify({
                'status': 'success',
                'projects': [],
                'raw_output': result['output']
            })
    else:
        return jsonify({
            'status': 'error',
            'error': result.get('error', result['stderr'])
        }), 500

@gcloud_bp.route('/config/get', methods=['GET'])
def get_config():
    """Возвращает текущую конфигурацию gcloud"""
    result = run_gcloud_command(['config', 'list', '--format=json'])
    
    if result['success']:
        try:
            config = json.loads(result['output'])
            return jsonify({
                'status': 'success',
                'config': config
            })
        except json.JSONDecodeError:
            return jsonify({
                'status': 'success',
                'config': {},
                'raw_output': result['output']
            })
    else:
        return jsonify({
            'status': 'error',
            'error': result.get('error', result['stderr'])
        }), 500

@gcloud_bp.route('/execute', methods=['POST'])
def execute_gcloud_command():
    """Выполняет произвольную команду gcloud"""
    try:
        data = request.get_json()
        if not data or 'command' not in data:
            return jsonify({'error': 'Команда не предоставлена'}), 400
        
        command = data['command']
        timeout = data.get('timeout', 30)
        
        # Разбиваем команду на аргументы (убираем 'gcloud' если он есть)
        if isinstance(command, str):
            command_args = command.split()
            if command_args and command_args[0] == 'gcloud':
                command_args = command_args[1:]
        else:
            command_args = command
        
        # Выполняем команду
        result = run_gcloud_command(command_args, timeout)
        
        return jsonify({
            'status': 'success' if result['success'] else 'error',
            'command': f"gcloud {' '.join(command_args)}",
            'returncode': result.get('returncode'),
            'output': result['output'],
            'stderr': result['stderr'],
            'error': result.get('error')
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': f'Ошибка при выполнении команды: {str(e)}'
        }), 500

@gcloud_bp.route('/auth/login-url', methods=['GET'])
def get_auth_login_url():
    """Возвращает URL для аутентификации (для использования в браузере)"""
    result = run_gcloud_command(['auth', 'login', '--no-launch-browser'])
    
    # Извлекаем URL из вывода
    output_lines = result['output'].split('\n') if result['output'] else []
    auth_url = None
    
    for line in output_lines:
        if 'https://accounts.google.com' in line:
            auth_url = line.strip()
            break
    
    if auth_url:
        return jsonify({
            'status': 'success',
            'auth_url': auth_url,
            'message': 'Откройте этот URL в браузере для аутентификации'
        })
    else:
        return jsonify({
            'status': 'error',
            'error': 'Не удалось получить URL для аутентификации',
            'output': result['output'],
            'stderr': result['stderr']
        }), 500

@gcloud_bp.route('/status', methods=['GET'])
def gcloud_status():
    """Проверяет статус Google Cloud CLI"""
    gcloud_path = get_gcloud_path()
    
    if not os.path.exists(gcloud_path):
        return jsonify({
            'status': 'not_installed',
            'message': 'Google Cloud CLI не установлен'
        })
    
    # Проверяем версию
    version_result = run_gcloud_command(['version'])
    if not version_result['success']:
        return jsonify({
            'status': 'error',
            'message': 'Google Cloud CLI установлен, но не работает корректно',
            'error': version_result.get('error', version_result['stderr'])
        })
    
    # Проверяем аутентификацию
    auth_result = run_gcloud_command(['auth', 'list'])
    authenticated = auth_result['success'] and 'ACTIVE' in auth_result['output']
    
    return jsonify({
        'status': 'installed',
        'authenticated': authenticated,
        'version': version_result['output'].strip(),
        'message': 'Google Cloud CLI готов к использованию' if authenticated else 'Google Cloud CLI установлен, но требует аутентификации'
    })
