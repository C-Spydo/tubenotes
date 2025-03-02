from app.models.user import User


def get_user_by_username(username: str):
    return User.query.filter_by(username=username).first()