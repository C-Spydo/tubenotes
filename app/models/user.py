from ..extensions.database import database
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import jsonpickle

class User(database.Model):
    __tablename__ = 'users'

    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(255), nullable=False)
    chats = relationship("Chat", back_populates="user", lazy="dynamic")  
    created_at = database.Column(database.DateTime(timezone=True), server_default=func.now())
    updated_at = database.Column(database.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f'<User {self.id}>'
    
    def  serialize(self):
        return {
            'username': self.username,
            "chats": [chat.serialize() for chat in self.chats]
        }
    
    def save_chat_memory(self, chat_data):
        self.chat_memory = jsonpickle.encode(chat_data)

    def deserialize_chat_memory(self):
        """Retrieve chat memory, handling empty cases"""
        if not self.chat_memory:
            return None  # Return an empty list if there's no stored chat memory
        try:
            return jsonpickle.decode(self.chat_memory)
        except Exception as e:
            print(f"Error decoding chat memory: {e}")
            return None