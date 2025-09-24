import os
import pty
import subprocess
import select
import termios
import struct
import fcntl
import signal
from threading import Thread
from flask import Blueprint, request
from flask_socketio import emit, disconnect
import json

terminal_bp = Blueprint('terminal', __name__)

# Глобальный словарь для хранения терминальных сессий
terminal_sessions = {}

class TerminalSession:
    def __init__(self, session_id, socketio):
        self.session_id = session_id
        self.socketio = socketio
        self.fd = None
        self.child_pid = None
        self.setup_terminal()
        
    def setup_terminal(self):
        """Создает новую терминальную сессию"""
        try:
            # Создаем псевдотерминал
            self.fd, slave_fd = pty.openpty()
            
            # Настраиваем окружение
            env = os.environ.copy()
            env['TERM'] = 'xterm-256color'
            env['PATH'] = env.get('PATH', '') + ':/home/ubuntu/web-terminal-app/google-cloud-sdk/bin'
            
            # Запускаем bash в псевдотерминале
            self.child_pid = os.fork()
            if self.child_pid == 0:
                # Дочерний процесс
                os.close(self.fd)
                os.setsid()
                os.dup2(slave_fd, 0)
                os.dup2(slave_fd, 1)
                os.dup2(slave_fd, 2)
                os.close(slave_fd)
                
                # Запускаем bash
                os.execve('/bin/bash', ['/bin/bash'], env)
            else:
                # Родительский процесс
                os.close(slave_fd)
                self.make_nonblocking()
                self.start_reading()
                
        except Exception as e:
            print(f"Ошибка при создании терминала: {e}")
            
    def make_nonblocking(self):
        """Делает файловый дескриптор неблокирующим"""
        flags = fcntl.fcntl(self.fd, fcntl.F_GETFL)
        fcntl.fcntl(self.fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)
        
    def start_reading(self):
        """Запускает поток для чтения вывода терминала"""
        def read_output():
            while True:
                try:
                    if self.fd is None:
                        break
                        
                    ready, _, _ = select.select([self.fd], [], [], 0.1)
                    if ready:
                        data = os.read(self.fd, 1024)
                        if data:
                            self.socketio.emit('terminal_output', {
                                'data': data.decode('utf-8', errors='ignore'),
                                'session_id': self.session_id
                            }, room=self.session_id)
                        else:
                            break
                except (OSError, ValueError):
                    break
                    
        thread = Thread(target=read_output, daemon=True)
        thread.start()
        
    def write_input(self, data):
        """Отправляет ввод в терминал"""
        try:
            if self.fd is not None:
                os.write(self.fd, data.encode('utf-8'))
        except (OSError, ValueError):
            pass
            
    def resize(self, rows, cols):
        """Изменяет размер терминала"""
        try:
            if self.fd is not None:
                winsize = struct.pack('HHHH', rows, cols, 0, 0)
                fcntl.ioctl(self.fd, termios.TIOCSWINSZ, winsize)
        except (OSError, ValueError):
            pass
            
    def close(self):
        """Закрывает терминальную сессию"""
        try:
            if self.child_pid:
                os.kill(self.child_pid, signal.SIGTERM)
            if self.fd is not None:
                os.close(self.fd)
                self.fd = None
        except (OSError, ValueError):
            pass

def init_terminal_socketio(socketio):
    """Инициализирует SocketIO события для терминала"""
    
    @socketio.on('connect')
    def handle_connect():
        print(f"Клиент подключен: {request.sid}")
        
    @socketio.on('disconnect')
    def handle_disconnect():
        print(f"Клиент отключен: {request.sid}")
        session_id = request.sid
        if session_id in terminal_sessions:
            terminal_sessions[session_id].close()
            del terminal_sessions[session_id]
            
    @socketio.on('create_terminal')
    def handle_create_terminal():
        session_id = request.sid
        if session_id not in terminal_sessions:
            terminal_sessions[session_id] = TerminalSession(session_id, socketio)
            emit('terminal_created', {'session_id': session_id})
        else:
            emit('terminal_created', {'session_id': session_id})
            
    @socketio.on('terminal_input')
    def handle_terminal_input(data):
        session_id = request.sid
        if session_id in terminal_sessions:
            terminal_sessions[session_id].write_input(data['input'])
            
    @socketio.on('terminal_resize')
    def handle_terminal_resize(data):
        session_id = request.sid
        if session_id in terminal_sessions:
            terminal_sessions[session_id].resize(data['rows'], data['cols'])
