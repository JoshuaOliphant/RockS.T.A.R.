import logging
import os
import openai
from logconfig import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


class OpenAI_API:

    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def create_assistant(self):
        return openai.beta.assistants.create(
            name="S.T.A.R. interviewing assistant",
            instructions="""You are a chatbot that interviews candidates for a  job. Your interview style is to use S.T.A.R. (Situation, Task, Action, Reasoning) to guide the candidate through a conversation. You should provide helpful feedback to the candidate.""",
            model="gpt-4-1106-preview")

    def create_thread(self):
        return openai.beta.threads.create()

    def create_message(self, user_input, thread):
        return openai.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=f"{user_input}")

    def create_run(self, thread, assistant):
        return openai.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id,
        )

    def wait_for_run_completion(self, run_created, thread):
        while True:
            run = openai.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run_created.id
            )
            if run.status == "completed":
                break
        return run

    def list_messages(self, thread):
        return openai.beta.threads.messages.list(
            thread_id=thread.id
        )
