from werkzeug.security import safe_str_cmp
from user import User


users = [
    User('20160686', 'renzodlc','123456'),
    User('20160685', 'cris','123456')
]

username_mapping = {u.username: u for u in users}

userid_mapping = {u.id: u for u in users}


def authenthicate(username, password):
    user = username_mapping.get(username, None)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)
