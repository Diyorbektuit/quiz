from django.template.context_processors import request
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User
from account import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError


# Create your views here.

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.RegisterSerializer
    permission_classes = (AllowAny, )


class LoginView(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        data = request.data
        email = data['email'] or None
        password = data['password'] or None

        user = User.objects.filter(email=email)


        if email is None:
            raise ValidationError(
                {
                    'msg': "email bo'sh bo'lishi mumkin emas"
                }
            )

        elif password is None:
            raise ValidationError(
                {
                    'msg': "password bo'sh bo'lishi mumkin emas"
                }
            )

        elif not user.exists():
            raise ValidationError(
                {
                    'msg': "Bunday user tizimda mavjud emas"
                }
            )

        elif user.exists() and not user.first().check_password(password):
            raise ValidationError(
                {
                    'msg': "email yoki parol notog'ri kiritildi"
                }
            )

        return Response(
            {
                "success": True,
                "user": user.first().email,
                "role": user.first().role,
                "access": user.first().tokens()['access'],
                "refresh": user.first().tokens()['refresh']
            },
            status=status.HTTP_200_OK
        )

class LogoutView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        user = request.user
        refresh_token = user.tokens()['refresh'] or None
        print(user.tokens()['access'] or None)

        if refresh_token is not None:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
                data = {
                    'msg': "Siz muvafaqiyatli tizimdan chiqdingiz"
                }

                return Response(data=data, status=status.HTTP_200_OK)

            except TokenError:
                data = {
                    'msg': "Token bilan bog'liq xatolik"
                }
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        else:
            data = {
                'msg': "Refresh token mavjud emas"
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        user = request.user
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response({"msg": "Parol muvaffaqiyatli yangilandi"}, status=200)
        return Response(
            {"msg": "Eski parolni noto'g'ri kiritdingiz!"},
            status=status.HTTP_400_BAD_REQUEST,
        )

class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method in ('PATCH', "PUT"):
            return serializers.ProfileSerializerForPut
        return serializers.ProfileSerializerForGet













