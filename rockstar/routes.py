from flask import Flask, request, render_template
from service import Service
from logconfig import setup_logging
import logging

app = Flask(__name__)
setup_logging()
app.logger = logging.getLogger(__name__)
service = Service()


@app.route('/', methods=['GET'])
def load():
    messages = service.load_existing_messages()
    html = ''
    for message in messages:
        app.logger.info(f"message: {message}")
        if message.role == 'user':
            user_input = message.content[0].text.value
            user_html = render_template(
                'user_message.html',
                user_input=user_input
            )
            html += user_html
        if message.role == 'assistant':
            assistant_output = message.content[0].text.value
            assistant_html = render_template(
                'assistant_message.html',
                assistant_output=assistant_output
            )
            html += assistant_html
    app.logger.info(f"html: {html}")

    return html


@app.route('/ask_star', methods=['GET', 'POST'])
def ask_star():
    question = request.form.get('question')
    app.logger.info(f"question: {question}")

    messages = service.submit_question(question)

    # Extract the assistant's answer from the messages
    answer = next((m.content for m in messages if m.role == 'assistant'), None)
    app.logger.debug(f"answer: {answer[0].text.value}")
    return render_template(
        'output.html',
        user_input=question,
        gpt_output=answer[0].text.value)
