from ..extensions.database import database
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class User(database.Model):
    __tablename__ = 'users'

    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    username = database.Column(database.String(255), nullable=False)
    email = database.Column(database.String(255), nullable=False)
    google_id = database.Column(database.String(255), nullable=False)
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