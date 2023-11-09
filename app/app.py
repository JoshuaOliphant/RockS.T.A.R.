from flask import Flask, request, render_template
import openai
import logging

from logconfig import setup_logging


def create_app():
    setup_logging()
    app = Flask(__name__)
    return app


app = create_app()
logger = logging.getLogger(__name__)


@app.route('/')
def chat_interface():
    return render_template('langui.html')


@app.route('/ask_gpt', methods=['POST'])
def ask_gpt():
    question = request.form.get('question')
    logger.info(f"question: {question}")
    # Make the API call
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"{question}"}],
        temperature=0.8
    )

    # Extract the generated text from the API response
    answer = response.choices[0].message.content
    # Return the user's question and GPT's answer
    return answer


if __name__ == "__main__":
    app.run(debug=True)
