from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

class EmailBackend(BaseBackend):
    def get_user(self, user_id):
        try:
            return get_user_model().objects.get(pk=user_id)
        except get_user_model().DoesNotExist:
            return None
        
    print("success")
        
    def authenticate(self, request, username=None, password=None):
        try:
            user = get_user_model().objects.get(Q(email__iexact=username) | Q(username__iexact=username))
            if user.check_password(password):
                return user
        except get_user_model().DoesNotExist:
            return None