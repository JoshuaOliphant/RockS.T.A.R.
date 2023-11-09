import logging
import os
import openai
from rich.console import Console

logger = logging.getLogger(__name__)


class Chatbot:

    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.assistant = openai.beta.assistants.create(
          name="S.T.A.R. interviewing assistant",
          instructions="""You are a chatbot that interviews candidates for a  job. Your interview style is to use S.T.A.R. (Situation, Task, Action, Reasoning) to guide the candidate through a conversation. You should provide helpful feedback to the candidate.""",
          model="gpt-4-1106-preview")

    def chat(self):
        thread = openai.beta.threads.create()
        console = Console()
        console.log("""Hi, I am a chatbot that interviews candidates for a job
                    Type 'exit' to end the conversation.""")

        while True:
            user_input = console.input("You: ")
            if user_input.lower() == "exit":
                break

            message = openai.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=f"{user_input}")

            run_created = openai.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=self.assistant.id,
            )

            while True:
                run = openai.beta.threads.runs.retrieve(
                  thread_id=thread.id,
                  run_id=run_created.id
                )
                console.log(f"Check status: {run.status}")
                if run.status == "completed":
                    break
            messages = openai.beta.threads.messages.list(
                thread_id=thread.id
                )
            assistant_response_id = messages.first_id
            retrieved_message = openai.beta.threads.messages.retrieve(
                thread_id=thread.id,
                message_id=assistant_response_id)
            console.log(retrieved_message.content[0].text.value)


if __name__ == "__main__":
    chatbot = Chatbot()
    chatbot.chat()
