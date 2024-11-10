from rest_framework import serializers

from .models import User
from .utils import is_valid_email

class RegisterSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=256, required=True)
    password = serializers.CharField(max_length=123, required=True)
    check_password = serializers.CharField(max_length=123, required=True)

    def create(self, validated_data):
        request = self.context.get('request')
        role = request.query_params.get('role') if request else None
        email = validated_data['email']
        password = validated_data['password']

        if role == "teacher":
            new_user = User.objects.create_user(email=email, password=password, role="teacher")
        else:
            new_user = User.objects.create_user(email=email, password=password)

        return new_user

    def validate(self, attrs):
        email = attrs['email']
        password = attrs['password']
        check_password = attrs['check_password']

        user = User.objects.filter(email=email)
        if user.exists():
            raise serializers.ValidationError(
                {
                    'msg': "Bu email orqali tizimga avval ro'yhatdan o'tilgan"
                }
            )

        if not is_valid_email(email):
            raise serializers.ValidationError(
                {
                    'msg': "email notog'ri kiritildi"
                }
            )

        if password != check_password:
            raise serializers.ValidationError(
                {
                    'msg': "Parollar mos kelmadi"
                }
            )


        return attrs

    def to_representation(self, instance):
        return {
            "success": True,
            "user": instance.email,
            "role": instance.role,
            "access": instance.tokens()['access'],
            "refresh": instance.tokens()['refresh']
        }


class ProfileSerializerForGet(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'profile_image'
        )

class ProfileSerializerForPut(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'profile_image',
        )

    def validate(self, attrs):
        first_name = attrs['first_name'] or "",
        last_name = attrs['last_name'] or "",

        if len(first_name) >= 20 or len(last_name) >= 20:
            raise serializers.ValidationError(
                detail={
                    'msg': "ism familya 20ta belgidan oshmashligi kerak"
                }
            )

        return attrs






