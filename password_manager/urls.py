from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from password_manager.views.auth.login import LoginView
from password_manager.views.auth.logout_all import LogoutAllView
from password_manager.views.auth.master_password.update_master_password import ChangeMasterPasswordView
from password_manager.views.auth.register import RegisterView, DeleteUserView
from password_manager.views.manager.category.create_category import CreateCategoryView, GetUsersCategoriesView, \
    DeleteCategoryView
from password_manager.views.manager.category.get_category import GetPasswordsByCategoryView
from password_manager.views.manager.create_password import CreatePasswordView
from password_manager.views.manager.delete_password import DeletePasswordView
from password_manager.views.manager.get_passwords import GetAllPasswordsView

urlpatterns = [
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/update-master-password/', ChangeMasterPasswordView.as_view(), name='update-master-password'),
    path('api/logout-all/', LogoutAllView.as_view(), name='logout-all'),
    path('api/delete-account/', DeleteUserView.as_view(), name='delete-account'),

    path('api/categories/', GetUsersCategoriesView.as_view(), name='get-users-categories'),
    path('api/create-category/', CreateCategoryView.as_view(), name='create-category'),
    path('api/delete-category/', DeleteCategoryView.as_view(), name='delete-category'),

    path('api/create-password/', CreatePasswordView.as_view(), name='create-password'),
    path('api/category/<int:category_id>/', GetPasswordsByCategoryView.as_view(), name='get-passwords-by-category'),
    path('api/passwords/', GetAllPasswordsView.as_view(), name='get-all-passwords'),
    path('api/delete-password/<int:password_id>/', DeletePasswordView.as_view(), name='delete-password'),
]
