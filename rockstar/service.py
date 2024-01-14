import os
from rockstar.database_manager import DatabaseManager
from sqlalchemy import create_engine
from rockstar.openai_api import OpenAI_API


class Service:
    def __init__(self) -> None:
        self._setup_db_manager()
        self.assistant = self.database_manager.get_assistant()
        self.openai_api = OpenAI_API()
        if self.assistant is None:
            self.assistant = self.openai_api.create_assistant()
            self.database_manager.save_assistant(self.assistant)
        self.thread = self.database_manager.get_thread()
        if self.thread is None:
            self.thread = self.openai_api.create_thread()
            self.database_manager.save_thread(self.thread)

    def load_existing_messages(self):
        return self.openai_api.list_messages(self.thread)

    def submit_question(self, question):
        self.openai_api.create_message(question, self.thread)
        run_created = self.openai_api.create_run(self.thread, self.assistant)
        self.openai_api.wait_for_run_completion(run_created, self.thread)
        return self.openai_api.list_messages(self.thread)

    def _setup_db_manager(self):
        db_name = os.environ.get("DB_NAME", "rockstar")
        db_path = f'{db_name}.sqlite'
        self.engine = create_engine(f'sqlite:///{db_path}')
        self.database_manager = DatabaseManager(self.engine)
        if not os.path.exists(db_path):
            self.database_manager.create_tables()
