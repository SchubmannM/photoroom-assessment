from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import Color
from .models import ColorPalette
from .models import CustomUser
from .models import Team
from .models import TeamMembership


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password")
        validated_data["username"] = validated_data["email"]
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
        model = Color
        fields = ("id", "hex_code")


class ColorPaletteSerializer(serializers.ModelSerializer):
    """
    Example output:
    {
        "id": "af045cf4-c654-448a-9d07-805fba73bd11",
        "name": "Different palette created by user b",
        "colors": [
            {
                "id": "981dfc4c-1f38-4999-ae74-71d97872acbe",
                "hex_code": "#aaaaaa"
            },
            {
                "id": "df17785d-c2f8-4074-bc81-ea4f22aff1cb",
                "hex_code": "#DADADA"
            }
        ],
        "created_by": {
            "id": "f37d8fef-6480-4f27-ae4b-1df3f782553e",
            "email": "some_other_user@gmail.com"
        }
    }
    """

    colors = ColorSerializer(many=True, read_only=True)
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = ColorPalette
        fields = ("id", "name", "colors", "created_by")


class TeamSerializer(serializers.ModelSerializer):
    """
    Example output:
    {
        "id": "28ccdc47-3245-4c52-a4e5-bcaeebf2f982",
        "name": "purrfect team",
        "color_palettes": [
            "af045cf4-c654-448a-9d07-805fba73bd11"
        ],
        "members": [
            {
                "id": "f37d8fef-6480-4f27-ae4b-1df3f782553e",
                "email": "some_other_user@gmail.com"
            }
        ]
    }
    """

    members = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ("id", "name", "color_palettes", "members")

    def get_members(self, instance):
        return UserSerializer(
            instance=CustomUser.objects.filter(
                id__in=TeamMembership.objects.filter(team=instance).values("user")
            ),
            many=True,
        ).data
