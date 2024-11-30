from datetime import date
import cryptography
from cryptography.fernet import Fernet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from password_manager.models import AuditLogs, MasterPasswordHistory, Password
from password_manager.views.manager.create_password import generate_key_from_master_password


class ChangeMasterPasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        current_password = request.data.get("current_password")
        new_password = request.data.get("new_password")


        if not current_password or not check_password(current_password, user.password):
            return Response({"error": "Current password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)

        if not new_password or len(new_password) < 8:
            return Response({"error": "New password must be at least 8 characters long"}, status=status.HTTP_400_BAD_REQUEST)

        user_old_hashed_password = user.password

        MasterPasswordHistory.objects.create(
            user=user,
            old_hashed_password=user.password,
            changed_at=date.today()
        )

        user.set_password(new_password)
        user.save()

        user_new_hashed_password = user.password

        AuditLogs.objects.create(
            user=user,
            action_type="PASSWORD_CHANGE",
            action_description="User changed their master password",
            created_at=date.today(),
        )

        key = generate_key_from_master_password(user_old_hashed_password)
        old_fernet = Fernet(key)

        new_key = generate_key_from_master_password(user_new_hashed_password)
        new_fernet = Fernet(new_key)

        passwords = Password.objects.filter(user=user)
        for password_obj in passwords:
            try:
                decrypted_password = old_fernet.decrypt(password_obj.encrypted_password.encode()).decode()
                encrypted_password = new_fernet.encrypt(decrypted_password.encode()).decode()
                password_obj.encrypted_password = encrypted_password
                password_obj.save()
            except (cryptography.fernet.InvalidToken, ValueError):
                return Response(
                    {"error": f"Failed to decrypt or re-encrypt password for service {password_obj.service_name}."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response({"message": "Master password changed successfully"}, status=status.HTTP_200_OK)