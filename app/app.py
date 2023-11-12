from flask import Flask, request, render_template
from chat import Chatbot

app = Flask(__name__)
chatbot = Chatbot()


@app.route('/')
def chat_interface():
    return render_template('langui.html')


@app.route('/ask_star', methods=['POST'])
def ask_star():
    question = request.form.get('question')
    app.logger.info(f"question: {question}")

    # Use the chatbot to get the response
    chatbot.create_message(question)
    run_created = chatbot.create_run()
    chatbot.wait_for_run_completion(run_created)
    messages = chatbot.list_messages()

    # Extract the assistant's answer from the messages
    answer = next((m.content for m in messages if m.role == 'assistant'), None)
    app.logger.debug(f"answer: {answer[0].text.value}")
    return render_template(
        'output.html',
        user_input=question,
        gpt_output=answer[0].text.value)
