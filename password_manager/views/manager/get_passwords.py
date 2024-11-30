from cryptography.fernet import Fernet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from password_manager.models import Password
from password_manager.views.manager.create_password import get_user_encryption_key, generate_key_from_encryption_key


class GetAllPasswordsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        passwords = Password.objects.filter(user=user)

        if not passwords.exists():
            return Response([], status=status.HTTP_200_OK)

        encryption_key = get_user_encryption_key(user)
        key = generate_key_from_encryption_key(encryption_key)
        fernet = Fernet(key)

        password_data = []
        for password in passwords:
            decrypted_password = fernet.decrypt(password.encrypted_password.encode()).decode()
            password_data.append({
                "id": password.id,
                "service_name": password.service_name,
                "username_for_service": password.username_for_service,
                "password": decrypted_password,
                "category_id": password.category.id if password.category else None,
                "created_at": password.created_at,
                "updated_at": password.updated_at
            })

        return Response(password_data, status=status.HTTP_200_OK)
