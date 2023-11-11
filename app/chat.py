import logging
import os
import openai
from rich.console import Console
from logconfig import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


class Chatbot:

    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.assistant = openai.beta.assistants.create(
          name="S.T.A.R. interviewing assistant",
          instructions="""You are a chatbot that interviews candidates for a  job. Your interview style is to use S.T.A.R. (Situation, Task, Action, Reasoning) to guide the candidate through a conversation. You should provide helpful feedback to the candidate.""",
          model="gpt-4-1106-preview")
        self.thread = openai.beta.threads.create()

    def create_message(self, user_input):
        message = openai.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=f"{user_input}")
        return message

    def create_run(self):
        run_created = openai.beta.threads.runs.create(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id,
        )
        return run_created

    def wait_for_run_completion(self, run_created):
        while True:
            run = openai.beta.threads.runs.retrieve(
                thread_id=self.thread.id,
                run_id=run_created.id
            )
            if run.status == "completed":
                break
        return run

    def list_messages(self):
        messages = openai.beta.threads.messages.list(
            thread_id=self.thread.id
        )
        return messages


if __name__ == "__main__":
    chatbot = Chatbot()
    chatbot.chat()
