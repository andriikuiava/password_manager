from rest_framework import serializers, generics
from rest_framework.permissions import IsAuthenticated
from password_manager.models import Password


class PasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Password
        fields = ['service_name', 'username_for_service', 'encrypted_password', 'category']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class PasswordCreateView(generics.CreateAPIView):
    serializer_class = PasswordSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)