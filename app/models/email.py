from ..extensions.database import database
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class Email(database.Model):
    __tablename__ = 'emails'

    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    prospect_id = database.Column(database.Integer, database.ForeignKey('prospects.id'), nullable=False)
    title = database.Column(database.String(100), nullable=False)
    message = database.Column(database.Text, nullable=False)
    status = database.Column(database.String(10), nullable=False)
    created_at = database.Column(database.DateTime(timezone=True), server_default=func.now())
    updated_at = database.Column(database.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    prospect = relationship("Prospect", back_populates="emails")

    def __repr__(self):
        return f'<Email {self.id}>'
    
    def serialize(self):
        return {
            "id": self.id,
            "contact_name": self.prospect["contact_name"],   
            "contact_email": self.prospect["contact_email"],   
            "title": self.title,
            "message": self.message,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }