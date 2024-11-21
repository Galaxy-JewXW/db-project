from django.shortcuts import render
from datetime import datetime
from rest_framework.response import Response
from rest_framework.views import APIView

from learingCompanionInBeihang.apps.users.models import User
from learingCompanionInBeihang.apps.utils.constants import *
from learingCompanionInBeihang.apps.utils.views import *


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

    @check_role(UserRole.ALL_USERS)
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


class ModifyUserInfo(APIView):

    @check_role(UserRole.ALL_USERS)
    def post(self, request, action_user: User = None):
        try:
            action_user.name = request.data['name']
            action_user.avatar = request.data['avatar']
            action_user.mail = request.data['mail']
            action_user.save()
        except Exception as _e:
            return Response(response_json(
                success=False,
                code=UserErrorCode.USER_SAVE_FAILED,
                message="can't save user!"
            ))
        return Response(response_json(
            success=True,
            message="modify user information successfully!"
        ))
