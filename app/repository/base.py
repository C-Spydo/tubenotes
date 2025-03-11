from ..extensions.database import session

def get_record_by_field(model, field, value):
    try:
        return session.query(model).filter(getattr(model, field) == value).first()
    except Exception as e:
        print(f"Error fetching record: {e}")
        return None
    
def get_list(model):
    try:
        return session.query(model).all()
    except Exception as e:
        print(f"Error fetching record: {e}")
        return None