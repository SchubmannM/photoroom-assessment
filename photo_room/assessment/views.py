from rest_framework.permissions import AllowAny
from .serializers import UserSerializer
from .models import CustomUser
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
def list_color_palettes(request):
    if request.method == 'GET':
        my_palettes = ColorPalette.objects.filter(created_by=request.user).prefetch_related('colors')
        serializer = ColorPaletteSerializer(instance=my_palettes, many=True)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)