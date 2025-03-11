from ..extensions.database import session
from flask import abort

def get_record_by_field(model, field, value):
    try:
        data = session.query(model).filter(getattr(model, field) == value).first()

        if data == None:
            abort(404, "Data not found")

        return data
    except Exception as e:
        print(f"Error fetching record: {e}")
        return None
    
def get_list(model):
    try:
        return session.query(model).all()
    except Exception as e:
        print(f"Error fetching record: {e}")
        return None