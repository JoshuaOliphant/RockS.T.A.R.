from flask import request, render_template, session, redirect, url_for
from rockstar.service import Service
from flask import Blueprint, current_app

service = Service()
bp = Blueprint('rockstar', __name__, url_prefix='/chat')


@bp.route('/')
def index():
    session.clear()
    return render_template('index.html', session_started=session.get('session_started', False))


@bp.route('/start_session', methods=['POST'])
def start_session():
    message = request.form['message']
    messages = process_message_and_get_response(message, is_initial=True)
    return render_template('chat.html', messages=messages)


@bp.route('/ask', methods=['POST'])
def ask():
    current_app.logger.info(f"User asked: {request.form}")
    message = request.form['message']
    current_app.logger.info(f"User asked: {message}")
    messages = process_message_and_get_response(message)
    return render_template('_messages.html', messages=messages)


# Utility function to process messages and get responses
def process_message_and_get_response(message, is_initial=False):
    # You might need to adjust this part to fit how your Service class works
    if is_initial:
        current_app.logger.info(f"User asked in start_session: {message}")
        service.initialize_assistant()
        current_app.logger.info("Assistant initialized.")
        service.initialize_thread()
        current_app.logger.info("Thread initialized.")
    response = service.submit_question(message)
    messages = [
        {"sender": "User", "content": message, "class": "user-message bg-blue-100 rounded p-2 text-blue-800"},
        {"sender": "Assistant", "content": response, "class": "assistant-message bg-green-100 rounded p-2 text-green-800"},
    ]
    return messages
