from app.extensions import database, session
from sqlalchemy.orm import relationship
from ..helpers import deserialize_json_data
from sqlalchemy.sql import func
import jsonpickle

class Chat(database.Model):
    __tablename__ = 'chats'

    id = database.Column(database.Integer, primary_key=True)
    user_id = database.Column(database.Integer, database.ForeignKey('users.id'), nullable=False)
    stock = database.Column(database.String(255), nullable=False)
    title = database.Column(database.String(255), nullable=True)
    memory = database.Column(database.Text, nullable=False)
    created_at = database.Column(database.DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="chats") 

    def __repr__(self):
        return f'<Chat {self.id}>'

    
    def serialize(self):
            return {
                'id': self.id,
                "stock": self.stock,
                "title": self.title,
                "memory": deserialize_json_data(self.memory)
            }
        
    def update_chat_memory(self, memory):
        self.memory = jsonpickle.encode(memory)
        session.commit()
