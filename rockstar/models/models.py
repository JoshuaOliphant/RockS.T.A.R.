from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Assistant(db.Model):
    __tablename__ = 'assistants'
    id = db.Column(db.String, primary_key=True)
    object_type = db.Column(db.String)
    created_at = db.Column(db.DateTime)
    name = db.Column(db.String)
    description = db.Column(db.String)
    model = db.Column(db.String)
    instructions = db.Column(db.String)
    tools = db.Column(db.JSON)
    file_ids = db.Column(db.JSON)
    assistant_metadata = db.Column(db.JSON)


class Threads(db.Model):
    __tablename__ = 'threads'
    id = db.Column(db.String, primary_key=True)
    object_type = db.Column(db.String)
    created_at = db.Column(db.DateTime)
    thread_metadata = db.Column(db.JSON)


class Messages(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.String, primary_key=True)
    object = db.Column(db.String)
    created_at = db.Column(db.DateTime)
    thread_id = db.Column(db.String)
    role = db.Column(db.String)
    content = db.Column(db.JSON)
    file_ids = db.Column(db.JSON)
    assistant_id = db.Column(db.String)
    run_id = db.Column(db.String)
    message_metadata = db.Column(db.JSON)
