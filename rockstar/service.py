from datetime import datetime
from flask import current_app

from rockstar.models.models import Assistant, db, Threads
from rockstar.openai_client import OpenAIClient


class Service:
    def __init__(self, openai_client=None):
        """Initialize the service with an OpenAI client.

        Args:
            openai_client (OpenAIClient): An instance of the OpenAIClient class.
        """
        self.openai_api = openai_client or OpenAIClient()
        self.assistant = None
        self.thread = None

    def initialize_assistant(self):
        """
        Initializes the assistant with customized instructions based on the user's input,
        or retrieves an existing assistant tailored to the same interview type.
        """
        # Get the only assistant
        current_app.logger.info("Initializing assistant")
        assistant_in_db = Assistant.query.first()
        current_app.logger.info(f"Assistant in DB: {assistant_in_db}")

        if assistant_in_db:
            current_app.logger.info("Using existing assistant tailored to the specified interview type from the database.")
            self.assistant = assistant_in_db
        else:
            current_app.logger.info("Creating a new assistant with customized instructions.")
            self.assistant = self.openai_api.create_assistant()
            self._add_assistant_to_db(self.assistant)
            self.thread = self.openai_api.create_thread()
            self._add_thread_to_db(self.thread)

    def _add_assistant_to_db(self, assistant):
        """Adds the assistant to the database."""
        try:
            created_at = self._convert_to_datetime(assistant.created_at)
            new_assistant = Assistant(
                id=self.assistant.id,
                object_type=self.assistant.object,
                created_at=created_at,
                name=self.assistant.name,
                description=self.assistant.description,
                model=self.assistant.model,
                instructions=self.assistant.instructions,
                tools=self.assistant.tools,
                file_ids=self.assistant.file_ids,
                assistant_metadata=self.assistant.metadata
            )
            db.session.add(new_assistant)
            db.session.commit()
            current_app.logger.info(f"Assistant {assistant.id} added to the database.")
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Failed to add assistant to DB: {e}")
            raise

    def initialize_thread(self):
        """Initializes the thread for the conversation."""
        self.thread = Threads.query.first()
        if not self.thread:
            self.thread = self.openai_api.create_thread()
            self._add_thread_to_db(self.thread)

    def _add_thread_to_db(self, thread):
        """Adds the thread to the database."""
        try:
            created_at = self._convert_to_datetime(thread.created_at)
            new_thread = Threads(
                id=thread.id,
                object_type=thread.object,
                created_at=created_at,
                thread_metadata=thread.metadata
            )
            db.session.add(new_thread)
            db.session.commit()
            current_app.logger.info(f"Thread {thread.id} added to the database.")
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Failed to add thread to DB: {e}")
            raise

    def _convert_to_datetime(self, timestamp):
        """Converts a timestamp to a datetime object."""
        return datetime.fromtimestamp(timestamp)

    def load_existing_messages(self):
        self.add_assistant_to_db()
        return self.openai_api.list_messages(self.thread)

    def submit_question(self, question):
        message = self.openai_api.create_message(question, self.thread)
        current_app.logger.info(f"Message created with content: {message.content} in thread {self.thread.id}.")
        run_created = self.openai_api.create_run(self.thread, self.assistant)
        current_app.logger.info(f"Run created {run_created.id}.")
        self.openai_api.wait_for_run_completion(run_created.id, self.thread.id)
        thread_messages = self.openai_api.list_messages(self.thread)
        return thread_messages.data[0].content[0].text.value
