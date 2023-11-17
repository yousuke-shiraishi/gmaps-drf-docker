from rest_framework import serializers
from .models import User, Gmap
from django.contrib.auth.hashers import make_password


class GmapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gmap
        fields = ['id', 'title', 'created_at', 'updated_at', 'comment', 'latitude', 'longitude', 'picture', 'magic_word', 'user']


class UserSerializer(serializers.ModelSerializer):
    gmaps = GmapSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'birth', 'gmaps', 'password']
        extra_kwargs = {'password': {'write_only': True}}  # パスワードは書き込み専用として設定

    def validate_password(self, value: str) -> str:
        """
        Hash value passed by user.

        :param value: password of a user
        :return: a hashed version of the password
        """
        return make_password(value)


