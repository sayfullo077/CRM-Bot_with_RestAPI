from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ShopSerializer, TelegramLinkCheckSerializer, ShopCreateSerializer
from account.managers import hmac_protected
from .models import Shop


class ShopCreateAPIView(APIView):
    @hmac_protected
    def post(self, request):
        print("==== Incoming Request ====")
        print("Data:", request.data)
        print("Headers:", request.headers)
        print("META:", request.META)

        language_code = request.data.get('language', 'uz')
        serializer = ShopCreateSerializer(data=request.data, context={'language_code': language_code})

        if not serializer.is_valid():
            print("ERRORS:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({"message": "Shop created successfully."}, status=status.HTTP_201_CREATED)
    
    
class ShopCheckLinkAPIView(APIView):
    @hmac_protected
    def post(self, request):
        serializer = TelegramLinkCheckSerializer(data=request.data)
        if serializer.is_valid():
            telegram_link = serializer.validated_data['telegram_link']
            exists = Shop.objects.filter(telegram_link=telegram_link).exists()
            return Response({'exists': exists}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)