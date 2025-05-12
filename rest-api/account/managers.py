from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
import hmac
import hashlib
import base64
import json
from django.conf import settings
from django.http import JsonResponse
from functools import wraps
import  time


def hmac_protected(view_func):
    @wraps(view_func)
    def _wrapped_view(self, request, *args, **kwargs):
        secret_key = settings.HMAC_SECRET_KEY.encode()
        django_request = request._request
        signature = django_request.META.get("HTTP_X_SIGNATURE")

        print("=== META HEADERS ===")
        for key, value in django_request.META.items():
            if "SIGNATURE" in key:
                print(f"{key}: {value}")
                
        if not signature:
            return JsonResponse({'error': 'Missing HMAC signature'}, status=401)

        try:
            payload = json.loads(request.body)

            # timestampni tekshirish
            timestamp = int(payload.get("timestamp", 0))
            now = int(time.time())
            if abs(now - timestamp) > 60:
                return JsonResponse({'error': 'Request expired'}, status=408)

            message = "&".join(f"{k}={v}" for k, v in sorted(payload.items()))
            expected_signature = hmac.new(secret_key, message.encode(), hashlib.sha256).digest()
            encoded_signature = base64.b64encode(expected_signature).decode()

            if not hmac.compare_digest(signature, encoded_signature):
                return JsonResponse({'error': 'Invalid HMAC signature'}, status=403)

        except Exception as e:
            return JsonResponse({'error': 'Invalid payload or internal error', 'detail': str(e)}, status=400)

        return view_func(self, request, *args, **kwargs)
    return _wrapped_view


class CustomUserManager(BaseUserManager):
    def _create_user(self, phone_number=None, password=None, **extra_fields):
        """
        Create and save a user with the given phone number or email and password.
        """
        if not phone_number and not extra_fields.get("email"):
            raise ValueError("The given phone_number or email must be set")

        if phone_number:
            user = self.model(phone_number=phone_number, **extra_fields)
        else:
            user = self.model(**extra_fields)

        if password:
            user.password = make_password(password)
            
        user.save(using=self._db)
        return user

    def create_user(self, phone_number=None, email=None, password=None, **extra_fields):
        if not phone_number and not email:
            raise ValueError("Either the phone number or email should be given")
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone_number=phone_number, password=password, email=email, **extra_fields)

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(phone_number=phone_number, password=password, **extra_fields)