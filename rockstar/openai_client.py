import logging
import os
import openai
from flask import current_app
from rockstar.logconfig import setup_logging
import backoff

setup_logging()
logger = logging.getLogger(__name__)


class OpenAIClient:

    def __init__(self, api_key=None):
        self.api_key = api_key if api_key is not None else os.getenv("OPENAI_API_KEY")
        openai.api_key = self.api_key

    def create_assistant(self, model="gpt-3.5-turbo"):
        return openai.beta.assistants.create(
            name="S.T.A.R. interviewing assistant",
            instructions="""
                You are a chatbot that interviews candidates for a job.
                Your interview style is to use S.T.A.R.
                (Situation, Task, Action, Reasoning) to guide the candidate
                through a conversation.
                You should provide helpful feedback to the candidate.""",
            model=model)

    def create_thread(self):
        return openai.beta.threads.create()

    def create_message(self, user_input, thread):
        current_app.logger.info(f"Creating message: {user_input}, in thread {thread.id}.")
        return openai.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=f"{user_input}")

    def create_run(self, thread, assistant):
        current_app.logger.info(f"Creating run in thread {thread.id} with assistant {assistant.id}.")
        return openai.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id,
        )

    def is_not_completed(run):
        """Check if the run status is not 'completed'. Other statuses to consider: 'expired', 'failed', 'cancelled'."""
        return run.status != "completed"

    @backoff.on_predicate(backoff.expo, is_not_completed, max_time=300, base=3)
    def wait_for_run_completion(self, run_id, thread_id):
        """Wait for a specific run to complete, with exponential backoff."""
        try:
            run = openai.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            if run.status == "completed":
                current_app.logger.info(f"Run {run_id} completed.")
                return run  # This will stop the backoff if run is completed
            if run.status in ["expired", "failed", "cancelled"]:
                current_app.logger.error(f"""
                                         Run {run_id} failed with status: {run.status}.
                                         Last error: {run.last_error}.
                                         """)
                raise Exception(f"Run {run_id} failed with status: {run.status}.")
            else:
                current_app.logger.info(f"Run {run_id} not completed yet. Status: {run.status}.")
                return run  # Backoff if not completed
        except Exception as e:
            current_app.logger.error(f"Error retrieving run {run_id}: {e}")
            raise  # This will stop the backoff due to an unexpected error

    def list_messages(self, thread):
        return openai.beta.threads.messages.list(
            thread_id=thread.id
        )
