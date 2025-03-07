from flask import abort
from app.models.chat import Chat


def get_chat_by_id(id: int) -> Chat:
    chat = Chat.query.filter_by(id=id).first()

    if chat is None:
        raise abort(404, "Chat not found")
    
    return chat