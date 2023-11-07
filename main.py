import os
import openai
import logging
from rich.logging import RichHandler

class Chatbot:
  def __init__(self):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    self.assistant = openai.beta.assistants.create(
      name="S.T.A.R. interviewing assistant",
      instructions=
      "You are a chatbot that interviews candidates for a job. Your interview style is to use S.T.A.R. (Situation, Task, Action, Reasoning) to guide the candidate through a conversation. You should provide helpful feedback to the candidate.",
      model="gpt-4-1106-preview")
    FORMAT = "%(message)s"
    logging.basicConfig(
        level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
    )

    self.log = logging.getLogger("starling")

  def chat(self):
    thread = openai.beta.threads.create()
    #prompt user for input
    print("Hi, I am a chatbot that interviews candidates for a job. Type 'exit' to end the conversation.")
    while True:
      #get user input
      user_input = input("You: ")
      if user_input.lower() == "exit":
        break
      
      openai.beta.threads.messages.create(
        thread_id=thread.id, 
        role="user", 
        content=f"{user_input}"
      )
      
      run = openai.beta.threads.runs.create(
          thread_id=thread.id,
          assistant_id=self.assistant.id,
      )
      
      while True:
        run = openai.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        print(f"Check status: {run.status}")
        # break out of the loop if the run is complete
        if run.status == "completed":
          break
      messages = openai.beta.threads.messages.list(thread_id=thread.id)
      print(messages)

if __name__ == "__main__":
  chatbot = Chatbot()
  chatbot.chat()
