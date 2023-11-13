from flask import Flask, request, render_template
from service import Service

app = Flask(__name__)
service = Service()


@app.route('/')
def chat_interface():
    return render_template('langui.html')


@app.route('/ask_star', methods=['POST'])
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
