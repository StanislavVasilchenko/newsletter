from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import UserRegistrationView, UserProfileView, UserVerifyView, UserDetailView, UserListView, \
    user_activity, UserDeleteView

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('verify/', UserVerifyView.as_view(), name='verify'),
    path('detail/', UserDetailView.as_view(), name='detail'),
    path('view_users/', UserListView.as_view(), name='view_users'),
    path('user_active/<int:pk>', user_activity, name='user_active'),
    path('user_delete/<int:pk>', UserDeleteView.as_view(), name='user_delete'),
]