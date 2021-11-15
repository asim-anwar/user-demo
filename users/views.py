from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
import jwt, datetime

from .serializers import *
from .models import *

# Create your views here.

class UserRegView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    users = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer_data = UserSerializer(data=request.data)
        if serializer_data.is_valid():
            serializer_data.save()
            response = {
                "message": "user create success",
                "status": status.HTTP_201_CREATED
            }
            return Response(response)

        else:
            response = {
                "message": "create error",
                "status": status.HTTP_400_BAD_REQUEST,
                "error": serializer_data.errors
            }
            return Response(response)

class UserLoginView(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        username = request.data['username']
        password = request.data['password']

        try:
            user = User.objects.get(username=username)

            if not authenticate(username=username, password=password):
                raise AuthenticationFailed('User with given username and password does not exists')

            payload = {
                'user_id': user.id,
                'email': user.email,
                'username': user.username,
                'is_superuser': user.is_superuser,
                'exp': datetime.datetime.utcnow()+datetime.timedelta(minutes=60),
                'iat': datetime.datetime.utcnow()
            }

            token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')

            response = Response()
            response.set_cookie(key='jwt', value=token, httponly=True)

            response.data = {
                'token': token,
                "message": user.full_name + " Logged In Successfully!"
            }

            return response

        except Exception as e:
            response = {
                'success': False,
                'statuscode': status.HTTP_400_BAD_REQUEST,
                'message': 'Invalid username or password',
                'Errors': str(e)
            }
            return Response(response)


class UserListView(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Authentication Failed! Please login first...')

        else:
            try:
                users = User.objects.all()
                serializer = UserSerializer(users, many=True)

                response = {
                    'success':True,
                    'statuscode':status.HTTP_200_OK,
                    'data':serializer.data,
                    'message': "View users Successful"
                }

                return Response(response)

            except Exception as e:
                response = {
                    'success': False,
                    'statuscode': status.HTTP_400_BAD_REQUEST,
                    'message': 'User list not found',
                    'Errors': str(e)
                }
                return Response(response)

class UserLogoutView(viewsets.ModelViewSet):

    def create(self, request, *args, **kwargs):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Already logged out!')

        else:
            response = Response()

            response.delete_cookie('jwt')
            response.data = {
                'message': 'You have been logged out!'
            }

            return response


