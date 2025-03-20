from http.client import HTTPException
from ..extensions.database import session
from flask import abort

def get_record_by_field(model, field, value):
    try:
        data = session.query(model).filter(getattr(model, field) == value).first()
        print(data)
        if data is None:
            abort(404, f"{model.__name__} not found")

        return data
    except HTTPException as e:
        print("something went wrong")
        pass

def get_records_by_field(model, field, value):
    try:
        data = session.query(model).filter(getattr(model, field) == value).all()
        return data
    except HTTPException as e:
        print("something went wrong")
        pass

def update_record_field(model, field, value):
    try:
        data = session.query(model).update(getattr(model, field) == value).first()
        print(data)
        if data is None:
            abort(404, f"{model.__name__} not found")

        return data
    except HTTPException as e:
        print("something went wrong")
        pass
        
    
def get_list(model):
    try:
        return session.query(model).all()
    except HTTPException as e:
        abort(500, "Something went wrong")
