from django.contrib.auth.hashers import check_password
from django.utils.timezone import now
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from password_manager.models import User, FailedLoginAttempts, AuditLogs
from password_manager.serializers import UserLoginSerializer


class LoginView(APIView):
    permission_classes = [AllowAny]

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            ip_address = self.get_client_ip(request)

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                FailedLoginAttempts.objects.create(
                    user=None,
                    ip_address=ip_address,
                    attempt_time=now(),
                    was_successful=False
                )
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

            if check_password(password, user.password):
                FailedLoginAttempts.objects.create(
                    user=user,
                    ip_address=ip_address,
                    attempt_time=now(),
                    was_successful=True
                )
                AuditLogs.objects.create(
                    user=user,
                    action_type='login',
                    action_description='User logged in. IP address: {}'.format(ip_address),
                    created_at=now()
                )
                refresh = RefreshToken.for_user(user)
                return Response({
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                }, status=status.HTTP_200_OK)
            else:
                FailedLoginAttempts.objects.create(
                    user=user,
                    ip_address=ip_address,
                    attempt_time=now(),
                    was_successful=False
                )
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)