from datetime import datetime
from sqlalchemy.orm import sessionmaker
from models import Assistant, Base


class DatabaseManager:
    def __init__(self, engine):
        self.engine = engine
        # Create a session factory
        self.Session = sessionmaker(bind=engine)

    def create_tables(self):
        Base.metadata.create_all(self.engine)

    def save_assistant(self, assistant):
        assistant_model = Assistant(
            id=assistant.id,
            object_type=assistant.object,
            created_at=datetime.fromtimestamp(assistant.created_at),
            name=assistant.name,
            description=assistant.description,
            model=assistant.model,
            instructions=assistant.instructions,
            tools=assistant.tools,
            file_ids=assistant.file_ids,
            metadata=assistant.metadata
        )
        session = self.Session()
        session.add(assistant_model)
        session.commit()
        session.close()

    def get_assistant(self):
        session = self.Session()
        assistant = session.query(Assistant).first()
        session.close()
        return assistant
