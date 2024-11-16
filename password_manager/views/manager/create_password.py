import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView

from password_manager.models import Category, Password
from datetime import date


def get_master_password(user):
    return user.password


def generate_key_from_master_password(master_password):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b'some_random_salt',
        iterations=100000
    )
    key = kdf.derive(master_password.encode())
    return base64.urlsafe_b64encode(key)


class CreatePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        category_id = request.data.get('category_id')
        service_name = request.data.get('service_name')
        password = request.data.get('password')
        username_for_service = request.data.get('username_for_service')

        user = request.user
        master_password = get_master_password(user)

        key = generate_key_from_master_password(master_password)
        fernet = Fernet(key)

        encrypted_password = fernet.encrypt(password.encode()).decode()

        category = None
        if category_id:
            category = get_object_or_404(Category, id=category_id, user=user)

        new_password = Password.objects.create(
            user=user,
            category=category,
            service_name=service_name,
            encrypted_password=encrypted_password,
            username_for_service=username_for_service,
            created_at=date.today(),
            updated_at=date.today()
        )

        return Response({
            "id": new_password.id,
            "service_name": new_password.service_name,
            "user": user.username,
            "category_id": category.id if category else None
        }, status=status.HTTP_201_CREATED)

