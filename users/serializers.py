from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'email', 'password']
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

# class UserLoginSerializer(serializers.Serializer):
#     username = serializers.CharField(max_length=255, required=False)
#     password = serializers.CharField(max_length=128, write_only=True)
#     token = serializers.CharField(max_length=255, read_only=True)
#
#     def validation(self, data):
#         username = data.get("username", None)
#         # email = data.get("username", None)
#         password = data.get("password", None)
#         user = authenticate(username=username, password=password)
#
#         if user is None:
#             raise serializers.ValidationError()