from app.extensions import database as db, session
from sqlalchemy.sql import func
import jsonpickle

from app.helpers import deserialize_json_data

class StockData(db.Model):
    __tablename__ = 'stock_data'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    news = db.Column(db.Text, nullable=False)
    stock_metadata = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f'<StockData {self.id}>'
    
    def serialize(self):
            return {
                'id': self.id,
                "news": self.news,
                "stock_metadata": deserialize_json_data(self.stock_metadata)
            }