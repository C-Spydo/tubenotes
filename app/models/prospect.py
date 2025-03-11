from app.extensions import database, session
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Prospect(database.Model):
    __tablename__ = 'prospects'

    id = database.Column(database.Integer, primary_key=True)
    industry_id = database.Column(database.Integer, nullable=False)
    company_name = database.Column(database.String(100), nullable=False) 
    contact_name = database.Column(database.String(100), nullable=False)
    contact_email = database.Column(database.String(100), nullable=False)
    contact_phone = database.Column(database.String(100), nullable=False)
    created_at = database.Column(database.DateTime(timezone=True), server_default=func.now())
    updated_at = database.Column(database.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    emails = relationship("Email", back_populates="prospect") 

    def __repr__(self):
        return f'<Prospect {self.id}>'
    
    def  serialize(self):
        return {
            "industry_id": self.industry_id,
            "company_name": self.company_name,
            "contact_name": self.contact_name,
            "contact_email": self.contact_email,
            "contact_phone": self.contact_phone
        }

    
  