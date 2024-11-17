from datetime import date
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from password_manager.models import AuditLogs, MasterPasswordHistory


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

        MasterPasswordHistory.objects.create(
            user=user,
            old_hashed_password=user.password,
            changed_at=date.today()
        )

        # Update the master password
        user.set_password(new_password)
        user.save()

        # Log the action in AuditLogs
        AuditLogs.objects.create(
            user=user,
            action_type="PASSWORD_CHANGE",
            action_description="User changed their master password",
            created_at=date.today(),
        )

        return Response({"message": "Master password changed successfully"}, status=status.HTTP_200_OK)