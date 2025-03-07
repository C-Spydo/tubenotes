from app.extensions import database as db, session
from sqlalchemy.sql import func
import jsonpickle


class StockData(db.Model):
    __tablename__ = 'stock_data'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    news = db.Column(db.Text, nullable=False)
    stock_metadata = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f'<StockData {self.id}>'
    
    def serialize(self):
            return {
                "name": self.name,
                "news": self.news,
                "stock_metadata": self.deserialize_stock_metadata()
            }
    
    def deserialize_stock_metadata(self):
        if not self.stock_metadata:
            return None 
        try:
            return jsonpickle.decode(self.stock_metadata)
        except Exception as e:
            print(f"Error decoding chat memory: {e}")
            return None