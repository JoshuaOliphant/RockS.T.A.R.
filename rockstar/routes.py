from flask import request, render_template
from rockstar.service import Service
from flask import Blueprint

service = Service()
bp = Blueprint('rockstar', __name__, url_prefix='/rockstar')


@bp.route('/', methods=['GET'])
def load():
    messages = service.load_existing_messages()
    html = ''
    for message in messages:
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

    return html


@bp.route('/ask_star', methods=['GET', 'POST'])
def ask_star():
    question = request.form.get('question')

    messages = service.submit_question(question)

    # Extract the assistant's answer from the messages
    answer = next((m.content for m in messages if m.role == 'assistant'), None)
    return render_template(
        'output.html',
        user_input=question,
        gpt_output=answer[0].text.value)
