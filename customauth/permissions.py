from rest_framework.permissions import BasePermission

from customauth.models import JWTToken


class IsTokenValid(BasePermission):
    def has_permission(self, request, view):
        token = request.META['HTTP_AUTHORIZATION'].split('JWT ')[1]
        if JWTToken.objects.filter(token=token, is_expired=False).count() > 0:
            return True
        else:
            return False
