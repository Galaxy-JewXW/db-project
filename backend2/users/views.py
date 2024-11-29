from django.shortcuts import render
from datetime import datetime
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from utils.constants import *
from utils.views import *


# Create your views here.

class UserSignUp(APIView):

    @check_role(UserRole.ALL_USERS)
    def post(self, request, action_user: User = None):
        student_id, name, password, mail, college, entryYear, avatar, role = request.data['student_id'], request.data[
            'name'], \
            request.data[
                'password'], request.data['mail'], request.data['college'], request.data['entryYear'], request.data[
            'avatar'], request.data['role']
        try:
            if User.objects.filter(student_id=student_id).exists():
                user = User.objects.get(student_id=student_id)
                user.name, user.password_digest, user.user_role = name, encode_password(password), role
                user.mail = mail if mail else f"{student_id}@buaa.edu.cn"
                user.college = college
                user.entryYear = entryYear
                user.avatar = avatar if avatar else DEFAULT_AVATAR
            else:
                mail_up = mail if mail else f"{student_id}@buaa.edu.cn"
                avatar_up = avatar if avatar else DEFAULT_AVATAR
                user = User(student_id=student_id, name=name, password_digest=encode_password(password),
                            mail=mail_up, college=college, entryYear=entryYear, user_role=role,
                            avatar=avatar_up)
            user.save()
        except Exception as _e:
            return Response(response_json(
                success=False,
                code=UserErrorCode.USER_SAVE_FAILED,
                message="can't save user!"
            ))
        # success
        return Response(response_json(
            success=True,
            message="user sign up successfully!"
        ))


class UserLogin(APIView):
    def post(self, request):
        # print(request.data)
        # get user
        try:
            # if no invalid id, User.objects.get will raise exception
            user = User.objects.get(student_id=request.data['student_id'])
        except Exception as _e:
            return Response(
                response_json(
                    success=False,
                    code=UserErrorCode.USER_NOT_FOUND,
                    message='user not found!'
                )
            )
        # check password
        try:
            password_digest = encode_password(request.data['password'])
            if password_digest != user.password_digest:
                raise Exception()
            jwt_token = generate_jwt(user.id)
            print(jwt_token)
            # print(jwt_token)
        except Exception as _e:
            return Response(response_json(
                success=False,
                code=UserErrorCode.INCORRECT_PASSWORD,
                message='incorrect password!'
            ))
        # login success
        return Response(
            response_json(
                success=True,
                message='login success!',
                data={
                    'jwt': jwt_token,
                    'role': user.user_role
                }
            )
        )


class UserLogout(APIView):
    @check_role(UserRole.ALL_USERS)
    def post(self, request, action_user: User = None):
        expired_token = BlackList(token=request.data['jwt'])
        expired_token.save()
        return Response(response_json(
            success=True,
            message="user logout successfully!"
        ))


class PasswordModify(APIView):

    @check_role(UserRole.ALL_USERS)
    def post(self, request, action_user: User = None):
        if action_user.password_digest != encode_password(request.data['password_old']):
            return Response(response_json(
                success=False,
                code=UserErrorCode.INCORRECT_PASSWORD,
                message='incorrect password!'
            ))
        try:
            action_user.password_digest = encode_password(request.data['password_new'])
            action_user.save()
        except Exception as _e:
            return Response(response_json(
                success=False,
                code=UserErrorCode.USER_SAVE_FAILED,
                message="can't save user!"
            ))
        return Response(response_json(
            success=True,
            message="modify password successfully!"
        ))
    
class GetUserInfo(APIView):
    # @check_role(UserRole.ALL_USERS)
    def post(self, request, action_user: User = None):
        return Response(response_json(
            success=True,
            message='get user information successfully!',
            data={
                'user_id': action_user.id,
                'student_id': action_user.student_id,
                'name': action_user.name,
                'mail': action_user.mail,
                'college': action_user.college,
                'entryYear': action_user.entryYear,
                'avatar': action_user.avatar,
                'role': action_user.user_role
            }
        ))

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
@method_decorator(csrf_exempt, name='dispatch')
class ModifyUserInfo(APIView):
    # @check_role(UserRole.ALL_USERS) 什么东西
    def post(self, request):
        try:
            # 从请求数据中获取 user_id
            user_id = request.data.get('user_id')
            if not user_id:
                return Response({
                    'success': False,
                    'message': 'User ID is required.'
                }, status=400)

            user = User.objects.get(student_id=user_id)  # 获取用户
            user.name = request.data.get('name')
            user.college = request.data.get('college')
            user.mail = request.data.get('mail')
            user.entryYear = request.data.get('year')
            # print(request.data.get('name'))
            # print(user.college)
            # print(user.mail)
            # print(user.entryYear)
            # user.save()
            # print(user)
        except User.DoesNotExist:
            return Response({
                'success': False,
                'message': 'User not found.'
            }, status=404)
        except Exception as _e:
            return Response({
                'success': False,
                'message': "Can't save user information."
            }, status=500)
        return Response({
            'success': True,
            'message': 'User information updated successfully.'
        })
