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


def get_user_encryption_key(user):
    return user.encryption_key


def generate_key_from_encryption_key(encryption_key):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b'some_random_salt',
        iterations=100000
    )
    key = kdf.derive(encryption_key.encode())
    return base64.urlsafe_b64encode(key)


class CreatePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        category_id = request.data.get('category_id')
        service_name = request.data.get('service_name')
        password = request.data.get('password')
        username_for_service = request.data.get('username_for_service')

        user = request.user
        encryption_key = get_user_encryption_key(user)

        key = generate_key_from_encryption_key(encryption_key)
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

class EditPasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, password_id):
        user = request.user
        password = Password.objects.filter(id=password_id, user=user).first()
        new_password = request.data.get('password')
        new_username = request.data.get('username_for_service')

        if not password:
            return Response({"error": "Password not found."}, status=status.HTTP_404_NOT_FOUND)

        encryption_key = get_user_encryption_key(user)
        key = generate_key_from_encryption_key(encryption_key)
        fernet = Fernet(key)

        encrypted_password = fernet.encrypt(new_password.encode()).decode()

        password.encrypted_password = encrypted_password
        password.username_for_service = new_username
        password.updated_at = date.today()
        password.save()

        return Response({"message": "Password updated successfully."}, status=status.HTTP_200_OK)

