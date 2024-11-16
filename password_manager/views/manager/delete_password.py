from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from password_manager.models import Password


class DeletePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, password_id):
        user = request.user

        try:
            # Retrieve the password object
            password = Password.objects.get(id=password_id, user=user)
        except Password.DoesNotExist:
            return Response({"error": "Password not found."}, status=status.HTTP_404_NOT_FOUND)

        # Delete the password
        password.delete()

        return Response({"message": "Password deleted successfully."}, status=status.HTTP_200_OK)