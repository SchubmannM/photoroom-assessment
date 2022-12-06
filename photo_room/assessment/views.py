from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSerializer
from .models import CustomUser, TeamMembership, TeamPalette
from rest_framework import generics
from rest_framework import permissions
from rest_framework import views
from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.auth import login
from . import serializers
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import AllowAny
from .serializers import *

class UserCreate(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class LoginView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = LoginSerializer(
            data=self.request.data, context={"request": self.request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        return Response(None, status=status.HTTP_202_ACCEPTED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_color_palette(request):
    if request.method == 'POST':
        name = request.data['name']
        colors = request.data['colors']
        palette, _ = ColorPalette.objects.get_or_create(name=name, created_by=request.user) # This might cause issues in the future - to refactor. Throw error if it already exists?
        for color in colors:
            color_instance, _ = Color.objects.get_or_create(hex_code=color)
            palette.colors.add(color_instance) # This can be optimise with a bulk_create and bulk add
        serializer = ColorPaletteSerializer(instance=palette, context={'request': request})
        data = serializer.data
        return Response(data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_color_palettes(request):
    if request.method == 'GET':
        my_palettes = ColorPalette.objects.filter(created_by=request.user).prefetch_related('colors')
        serializer = ColorPaletteSerializer(instance=my_palettes, many=True)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_team(request):
    if request.method == 'POST':
        name = request.data['name']
        team, _ = Team.objects.get_or_create(name=name)
        serializer = TeamSerializer(instance=team, context={'request': request})
        data = serializer.data
        return Response(data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])
def join_team(request):
    if request.method == 'POST':
        id = request.data['id']
        try:
            team = Team.objects.get(id=id)
        except Team.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        membership, _ = TeamMembership.objects.get_or_create(user=request.user, team=team)
        serializer = TeamSerializer(instance=team, context={'request': request})
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def list_teams(request):
    if request.method == 'GET':
        user = request.user
        try:
            memberships = TeamMembership.objects.filter(user=user)
        except Team.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        teams = Team.objects.filter(id__in=memberships.values('team'))
        serializer = TeamSerializer(instance=teams, many=True, context={'request': request})
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def assign_palette_to_team(request):
    if request.method == 'POST':
        palette_id = request.data['palette_id']
        team_id = request.data['team_id']
        try:
            membership = TeamMembership.objects.get(user=request.user, team=team_id)
        except TeamMembership.DoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED) # Membership not found -> Not part of the team or team doesnt exist.
        try:
            color_palette = ColorPalette.objects.get(id=palette_id)
        except ColorPalette.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        team_palette, _ = TeamPalette.objects.get_or_create(team=membership.team, palette=color_palette)
        serializer = TeamSerializer(instance=team_palette.team, context={'request': request})
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)