from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from datetime import date
from password_manager.models import Category


class GetUsersCategoriesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        categories = Category.objects.filter(user=user)
        data = []
        for category in categories:
            data.append({
                "id": category.id,
                "name": category.name,
                "user": user.username,
                "created_at": category.created_at,
                "updated_at": category.updated_at
            })
        return Response(data, status=status.HTTP_200_OK)

class CreateCategoryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        category_name = request.data.get('name')

        if not category_name:
            return Response({"error": "Category name is required."}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        if Category.objects.filter(user=user, name=category_name).exists():
            return Response({"error": "Category with this name already exists."}, status=status.HTTP_400_BAD_REQUEST)

        category = Category.objects.create(
            user=user,
            name=category_name,
            created_at=date.today(),
            updated_at=date.today()
        )
        return Response({
            "id": category.id,
            "name": category.name,
            "user": user.username,
            "created_at": category.created_at,
            "updated_at": category.updated_at
        }, status=status.HTTP_201_CREATED)


class DeleteCategoryView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        category_id = request.data.get('category_id')
        user = request.user
        try:
            category = Category.objects.get(id=category_id, user=user)
        except Category.DoesNotExist:
            return Response({"error": "Category not found."}, status=status.HTTP_404_NOT_FOUND)

        category.delete()
        return Response({"message": "Category deleted successfully."}, status=status.HTTP_200_OK)
