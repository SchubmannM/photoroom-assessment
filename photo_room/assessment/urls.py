from django.urls import path
from .views import UserCreate,LoginView, create_color_palette, list_color_palettes

urlpatterns = [
    path('account/register', UserCreate.as_view(), name="create_user"),
    path('account/login', LoginView.as_view(), name="login"),
    path('color_palette/create', create_color_palette, name="create_color_palette"),
    path('color_palette/list', list_color_palettes, name='list_color_palettes')
]
