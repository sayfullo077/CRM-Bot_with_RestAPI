import requests
from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.response import Response
from .models import Shop
from core import settings
from account.models import User
from common.models import Media


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['id', 'user', 'image', 'url', 'title']
        

class ShopCreateSerializer(serializers.ModelSerializer):
    telegram_id = serializers.IntegerField(write_only=True)
    image = serializers.CharField(write_only=True)
    language = serializers.CharField(write_only=True, required=False)

    # Multi-language title and desc fields
    title_uz = serializers.CharField(required=False, allow_blank=True)
    title_ru = serializers.CharField(required=False, allow_blank=True)
    title_en = serializers.CharField(required=False, allow_blank=True)
    title_uk = serializers.CharField(required=False, allow_blank=True)
    
    desc_uz = serializers.CharField(required=False, allow_blank=True)
    desc_ru = serializers.CharField(required=False, allow_blank=True)
    desc_en = serializers.CharField(required=False, allow_blank=True)
    desc_uk = serializers.CharField(required=False, allow_blank=True)

    telegram_link = serializers.URLField(required=False, allow_blank=True)

    class Meta:
        model = Shop
        fields = (
            'telegram_id',
            'image',
            'language',
            'title_uz', 'title_ru', 'title_en', 'title_uk',
            'desc_uz', 'desc_ru', 'desc_en', 'desc_uk',
            'telegram_link'
        )

    def create(self, validated_data):
        telegram_id = validated_data.pop('telegram_id')
        image_file_id = validated_data.pop('image')
        language = validated_data.pop('language', 'uz')

        title_field = f'title_{language}'
        desc_field = f'desc_{language}'

        title_value = validated_data.get(title_field)
        desc_value = validated_data.get(desc_field)

        if not title_value:
            raise serializers.ValidationError({title_field: f"Title in '{language}' is required."})
        if not desc_value:
            raise serializers.ValidationError({desc_field: f"Description in '{language}' is required."})

        try:
            user = User.objects.get(telegram_id=telegram_id)
        except User.DoesNotExist:
            raise serializers.ValidationError({"user": "User with the given telegram_id does not exist."})

        # Avval getFile chaqiramiz
        get_file_url = f"https://api.telegram.org/bot{settings.BOT_TOKEN}/getFile?file_id={image_file_id}"
        file_info_response = requests.get(get_file_url)
        if file_info_response.status_code != 200:
            raise serializers.ValidationError({"image": "Failed to fetch image file info from Telegram."})

        file_info_json = file_info_response.json()
        file_path = file_info_json['result']['file_path']

        # Endi haqiqiy file olish
        download_url = f"https://api.telegram.org/file/bot{settings.BOT_TOKEN}/{file_path}"
        file_response = requests.get(download_url)
        if file_response.status_code != 200:
            raise serializers.ValidationError({"image": "Failed to download image from Telegram."})

        file_name = f"{image_file_id}.jpg"
        file_content = file_response.content
        image = ContentFile(file_content, name=file_name)

        media = Media.objects.create(type=Media.MediaType.IMAGE, file=image)

        # Shop yaratish
        shop = Shop.objects.create(
            user=user,
            image=media,
            telegram_link=validated_data.get('telegram_link', ''),
            **{
                title_field: title_value,
                desc_field: desc_value
            }
        )

        return shop
        
    
class TelegramLinkCheckSerializer(serializers.Serializer):
    telegram_link = serializers.CharField(max_length=100)
    