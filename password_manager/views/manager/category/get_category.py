from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from password_manager.models import Password, Category
from cryptography.fernet import Fernet
from password_manager.views.auth.register import generate_encryption_key


class GetPasswordsByCategoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, category_id):
        user = request.user
        try:
            category = Category.objects.get(id=category_id, user=user)
        except Category.DoesNotExist:
            return Response({"error": "Category not found."}, status=status.HTTP_404_NOT_FOUND)

        passwords = Password.objects.filter(category=category, user=user)

        if not passwords.exists():
            return Response({"error": "No passwords found for this category."}, status=status.HTTP_404_NOT_FOUND)

        encryption_key = generate_encryption_key(user.password)
        fernet = Fernet(encryption_key)

        password_data = []
        for password in passwords:
            decrypted_password = fernet.decrypt(password.encrypted_password.encode()).decode()
            password_data.append({
                "id": password.id,
                "service_name": password.service_name,
                "username_for_service": password.username_for_service,
                "password": decrypted_password,
                "created_at": password.created_at,
                "updated_at": password.updated_at
            })

        return Response(password_data, status=status.HTTP_200_OK)