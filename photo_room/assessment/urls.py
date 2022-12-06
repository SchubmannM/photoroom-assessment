from django.urls import path

from .views import assign_palette_to_team
from .views import create_color_palette
from .views import create_team
from .views import join_team
from .views import list_color_palettes
from .views import list_teams
from .views import LoginView
from .views import UserCreate

urlpatterns = [
    path("account/register", UserCreate.as_view(), name="create_user"),
    path("account/login", LoginView.as_view(), name="login"),
    path("color_palette/create", create_color_palette, name="create_color_palette"),
    path("color_palette/list", list_color_palettes, name="list_color_palettes"),
    path(
        "color_palette/assign_to_team",
        assign_palette_to_team,
        name="assign_palette_to_team",
    ),
    path("team/create", create_team, name="create_team"),
    path("team/join", join_team, name="join_team"),
    path("team/list", list_teams, name="list_teams"),
]
