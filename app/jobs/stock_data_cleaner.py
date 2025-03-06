from ..models import StockData
from ..extensions import session
from datetime import datetime, timedelta

def clean_stock_table(app):
    with app.app_context():
        print('cleaning db')
        cutoff_time = datetime.now() - timedelta(hours=24)
        session.query(StockData).filter(StockData.created_at < cutoff_time).delete(synchronize_session=False)
        session.commit()