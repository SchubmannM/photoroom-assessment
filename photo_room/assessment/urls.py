from django.urls import path
from .views import UserCreate,LoginView

urlpatterns = [
    path('account/register', UserCreate.as_view(), name="create_user"),
    path('account/login', LoginView.as_view(), name="login"),
]
