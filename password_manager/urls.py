from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from password_manager.views.auth.login import LoginView
from password_manager.views.auth.register import RegisterView
from password_manager.views.manager.category.create_category import CreateCategoryView, GetUsersCategoriesView, \
    DeleteCategoryView
from password_manager.views.manager.category.get_category import GetPasswordsByCategoryView
from password_manager.views.manager.create_password import CreatePasswordView
from password_manager.views.manager.delete_password import DeletePasswordView
from password_manager.views.manager.get_passwords import GetAllPasswordsView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('categories/', GetUsersCategoriesView.as_view(), name='get-users-categories'),
    path('create-category/', CreateCategoryView.as_view(), name='create-category'),
    path('delete-category/', DeleteCategoryView.as_view(), name='delete-category'),

    path('create-password/', CreatePasswordView.as_view(), name='create-password'),
    path('category/<int:category_id>/', GetPasswordsByCategoryView.as_view(), name='get-passwords-by-category'),
    path('passwords/', GetAllPasswordsView.as_view(), name='get-all-passwords'),
    path('delete-password/<int:password_id>/', DeletePasswordView.as_view(), name='delete-password'),
]
