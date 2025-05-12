from rest_framework import serializers
from shop.serializers import ShopSerializer
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'telegram_id', 'fullname', 'firstname', 'lastname', 'notification', 'phone_number', 'password', 'role', 'ordered', 'language', 'shops']


class PhoneNumberCheckSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20)


class UserUpdatePhoneLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['language', 'phone_number']


class UserUpdateLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['telegram_link']

    def validate_telegram_link(self, value):
        if not value.startswith("https://t.me/"):
            raise serializers.ValidationError("Telegram link must start with https://t.me/")
        return value
  
        
class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "telegram_id",
            "username",
            "fullname",
            "firstname",
            "lastname",
            "language",
        ]
        