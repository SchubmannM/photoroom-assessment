from rest_framework import serializers
from .models import CustomUser, ColorPalette, Color
from django.contrib.auth import authenticate

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password")
        validated_data['username'] = validated_data['email']
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(label="Email", write_only=True)
    password = serializers.CharField(
        label="Password",
        # This will be used when the DRF browsable API is enabled
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        if email and password:
            user = authenticate(
                request=self.context.get("request"), username=email, password=password
            )
            if not user:
                msg = "Access denied: wrong email or password."
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = 'Both "email" and "password" are required.'
            raise serializers.ValidationError(msg, code="authorization")
        attrs["user"] = user
        return attrs


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model= Color
        fields = ('id', 'hex_code')


class ColorPaletteSerializer(serializers.ModelSerializer):
    colors = ColorSerializer(many=True, read_only=True)
    created_by = UserSerializer(read_only=True)
    class Meta:
        model = ColorPalette
        fields = ('id', 'name', 'colors', 'created_by')

