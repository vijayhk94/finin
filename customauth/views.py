# Create your views here.

from rest_auth.registration.views import RegisterView
from rest_auth.views import LoginView, LogoutView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from customauth.models import JWTToken
from customauth.permissions import IsTokenValid


class CustomRegisterView(RegisterView):
    def perform_create(self, serializer):
        user = super(CustomRegisterView, self).perform_create(serializer)
        JWTToken.objects.create(user_id=user.id, token=self.token)
        return user


class CustomLoginView(LoginView):
    def login(self):
        super(CustomLoginView, self).login()
        JWTToken.objects.create(user_id=self.user.id, token=self.token)


class CustomLogoutView(LogoutView):
    def logout(self, request):
        response = super(CustomLogoutView, self).logout(request)
        if response.status_code == 200:
            token = request.META['HTTP_AUTHORIZATION'].split('JWT ')[1]
            qs = JWTToken.objects.filter(token=token)
            qs.update(is_expired=True)
        return response


class ForceLogoutView(APIView):
    permission_classes = (IsTokenValid,)

    def force_logout(self, request):
        token = request.META['HTTP_AUTHORIZATION'].split('JWT ')[1]
        user = JWTToken.objects.get(token=token).user
        if not user.is_superuser:
            return Response(status=status.HTTP_403_FORBIDDEN)
        qs = JWTToken.objects.filter(user_id=request.data.get('user_id'))
        qs.update(is_expired=True)
        return Response(status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        return self.force_logout(request)


class TestView(APIView):
    permission_classes = (IsTokenValid,)

    def test_api(self, request):
        return Response(status=status.HTTP_200_OK, data={"msg": "access was allowed."})

    def post(self, request, *args, **kwargs):
        return self.test_api(request)
