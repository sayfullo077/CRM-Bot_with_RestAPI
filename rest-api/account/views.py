from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from django.core.exceptions import ObjectDoesNotExist
from .models import User
from .serializers import UserSerializer, UserCreateSerializer, PhoneNumberCheckSerializer, UserUpdatePhoneLanguageSerializer, UserUpdateLinkSerializer
from .managers import hmac_protected


class GetUserAPIView(APIView):
    def get(self, request, telegram_id):
        try:
            user = User.objects.get(telegram_id=telegram_id)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


# 2. Barcha userlar ro'yxatini chiqaruvchi class
class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    

class UserCreateAPIView(APIView):
    @hmac_protected
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created'}, status=status.HTTP_201_CREATED)
        print("ERRORS:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserCheckPhoneAPIView(APIView):
    @hmac_protected
    def post(self, request):
        serializer = PhoneNumberCheckSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            exists = User.objects.filter(phone_number=phone_number).exists()
            return Response({'exists': exists}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UpdateUserPhoneLanguageView(APIView):
    @hmac_protected
    def post(self, request):
        telegram_id = request.data.get("telegram_id")
        language = request.data.get("language")
        phone_number = request.data.get("phone_number")

        if not telegram_id:
            return Response({'error': "Telegram_id is required."}, status=status.HTTP_400_BAD_REQUEST)
        if not language:
            return Response({'error': "Language is required."}, status=status.HTTP_400_BAD_REQUEST)
        if not phone_number:
            return Response({'error': "Phone_number is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(telegram_id=telegram_id)
            serializer = UserUpdatePhoneLanguageSerializer(data=request.data)
            if serializer.is_valid():
                user.language = serializer.validated_data.get('language', user.language)
                user.phone_number = serializer.validated_data.get('phone_number', user.phone_number)
                user.save()
                return Response({"message": "User updated successfully."}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except ObjectDoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
        
class UpdateUserLinkView(APIView):
    @hmac_protected
    def post(self, request):
        telegram_id = request.data.get("telegram_id")
        telegram_link = request.data.get("telegram_link")
        
        if not telegram_id:
            return Response({'error': "Telegram_id is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not telegram_link:
            return Response({'error': "Telegram Link is required."}, status=status.HTTP_400_BAD_REQUEST)
       
        try:
            user = User.objects.get(telegram_id=telegram_id)
            serializer = UserUpdateLinkSerializer(data=request.data)
            if serializer.is_valid():
                user.telegram_link = serializer.validated_data.get('telegram_link', user.telegram_link)
                user.save()
                return Response({"message": "User link updated successfully."}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except ObjectDoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)