from ribo_api.models.user import User
from ribo_api.services.base import BaseService


class UserService(BaseService):
    
    @classmethod
    def get_user(cls, user_id):
        obj = User.objects(id=user_id)
        if len(obj) == 0:
            return False
        return obj[0]