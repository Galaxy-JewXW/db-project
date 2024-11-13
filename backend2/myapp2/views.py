# myapp/views.py

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, LoginSerializer

class AuthView(APIView):
    """
    处理用户登录和注册请求。
    如果请求中包含注册所需的字段（如 email 和 password_confirm），则执行注册操作。
    否则，执行登录操作。
    """
    def post(self, request):
        # 如果请求数据中包含 `email` 和 `password_confirm`，则视为注册请求
        if 'email' in request.data and 'password_confirm' in request.data:
            # 注册操作
            serializer = RegisterSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Registration successful"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # 否则视为登录请求
        else:
            # 登录操作
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid():
                username = serializer.data.get('username')
                password = serializer.data.get('password')
                user = authenticate(username=username, password=password)
                if user:
                    return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
