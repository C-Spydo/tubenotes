from ..extensions.database import database
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class Email(database.Model):
    __tablename__ = 'emails'

    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    prospect_id = database.Column(database.Integer, database.ForeignKey('prospects.id'), nullable=False)
    message = database.Column(database.Text, nullable=False)
    created_at = database.Column(database.DateTime(timezone=True), server_default=func.now())
    updated_at = database.Column(database.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    prospect = relationship("Prospect", back_populates="emails")

    def __repr__(self):
        return f'<Email {self.id}>'
    
    def serialize(self):
        return {
            "id": self.id,
            "contact_email": self.prospect["contact_email"],   
            "message": self.message,
            "created_at": self.created_at
        }