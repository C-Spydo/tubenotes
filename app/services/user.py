from app.helpers import add_record_to_database
from app.models.user import User
from app.repository.user import get_user_by_username


def sign_in(username: str):
    user = get_user_by_username(username)

    if user is None:
        user = User(username=username)
        add_record_to_database(user)

    serialized_user = user.serialize()

    chat_memories = serialized_user['chats']

    for chat_memory in chat_memories:
        if chat_memory is not None:
            chat_memory = chat_memory.load_memory_variables({})["history"]

    return serialized_user