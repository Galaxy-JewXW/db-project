from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from .models import Broadcast
from utils.views import decode_request
from users.models import User


class PublishBroadcast(APIView):
    """
    发布新的广播消息。
    """

    def post(self, request):
        try:
            data = decode_request(request)
            user_id = data.get('user_id')
            user = User.objects.get(student_id=user_id)
            # sender = data.get("sender")  # 默认发件人名字为"系统通知"
            sender = user.name
            title = data.get("title")
            content = data.get("content")
            print(user_id)

            if user.user_role != 1:
                return Response({
                    "success": False,
                    "error": "权限不足",
                    "message": "权限不足"
                }, status=HTTP_400_BAD_REQUEST)
            print(user.user_role)
            # 创建新的广播消息
            broadcast = Broadcast.objects.create(sender=sender, title=title, content=content)

            return Response({
                "success": True,
                "message": "Broadcast published successfully.",
                "broadcast_id": broadcast.id,
                "broadcast_details": {
                    "sender": broadcast.sender,
                    "sent_at": broadcast.sent_at,
                    "content": broadcast.content,
                }
            }, status=HTTP_200_OK)

        except User.DoesNotExist:
            return Response({
                'success': False,
                'error': 'User not found'
            }, status=HTTP_404_NOT_FOUND)

        except KeyError:
            return Response({
                "success": False,
                "error": "Missing required field: 'content'."
            }, status=HTTP_400_BAD_REQUEST)


class EditBroadcast(APIView):
    """
    编辑现有广播消息。
    """

    def post(self, request):
        try:
            data = decode_request(request)
            user_id = data.get('user_id')
            user = User.objects.get(student_id=user_id)
            broadcast_id = data.get("broadcast_id")
            new_title = data.get("title")
            new_content = data.get("content")
            print(new_content)
            if user.user_role != 1:
                return Response({
                    "success": False,
                    "error": "权限不足",
                    "message": "权限不足"
                }, status=HTTP_400_BAD_REQUEST)

            # 查找广播
            try:
                broadcast = Broadcast.objects.get(id=broadcast_id)
            except Broadcast.DoesNotExist:
                return Response({
                    "success": False,
                    "error": "Broadcast not found."
                }, status=HTTP_404_NOT_FOUND)

            # 更新广播内容
            broadcast.title = new_title if new_title else broadcast.title  # 如果未提供新标题，保持原标题
            broadcast.content = new_content if new_content else broadcast.content
            broadcast.save()

            return Response({
                "success": True,
                "message": "Broadcast updated successfully.",
                "broadcast_details": {
                    "sender": broadcast.sender,
                    "sent_at": broadcast.sent_at,
                    "title": broadcast.title,
                    "last_updated": broadcast.last_updated,  # 返回最新更新时间
                    "content": broadcast.content,
                }
            }, status=HTTP_200_OK)

        except User.DoesNotExist:
            return Response({
                'success': False,
                'error': 'User not found'
            }, status=HTTP_404_NOT_FOUND)

        except KeyError:
            return Response({
                "success": False,
                "error": "Missing required fields."
            }, status=HTTP_400_BAD_REQUEST)


class DeleteBroadcast(APIView):
    """
    删除广播消息。
    """

    def post(self, request):
        try:
            data = decode_request(request)
            user_id = data.get('user_id')
            user = User.objects.get(student_id=user_id)
            broadcast_id = data.get("broadcast_id")

            if user.user_role != 1:
                return Response({
                    "success": False,
                    "error": "权限不足",
                    "message": "权限不足"
                }, status=HTTP_400_BAD_REQUEST)

            # 查找并删除广播
            try:
                broadcast = Broadcast.objects.get(id=broadcast_id)
                broadcast.delete()
                return Response({
                    "success": True,
                    "message": "Broadcast deleted successfully."
                }, status=HTTP_200_OK)

            except Broadcast.DoesNotExist:
                return Response({
                    "success": False,
                    "error": "Broadcast not found."
                }, status=HTTP_404_NOT_FOUND)

        except User.DoesNotExist:
            return Response({
                'success': False,
                'error': 'User not found'
            }, status=HTTP_404_NOT_FOUND)

        except KeyError:
            return Response({
                "success": False,
                "error": "Missing required fields."
            }, status=HTTP_400_BAD_REQUEST)


class GetAllBroadcasts(APIView):
    """
    获取所有广播消息（仅管理员权限）。
    """

    def post(self, request):
        data = decode_request(request)
        user_id = data.get('user_id')
        print(user_id)
        try:
            # 获取用户信息
            user = User.objects.get(student_id=user_id)

            if user.user_role < 1:
                return Response({
                    "success": False,
                    "error": "权限不足",
                    "message": "权限不足"
                }, status=HTTP_400_BAD_REQUEST)

            # 获取所有广播消息
            broadcasts = Broadcast.objects.all().order_by("-sent_at")

            # 构造返回数据
            broadcasts_data = []
            for broadcast in broadcasts:
                broadcasts_data.append({
                    "id": broadcast.id,
                    "publisher": broadcast.sender,
                    "sent_at": broadcast.sent_at,
                    "releaseTime": broadcast.last_updated,
                    "title": broadcast.title,
                    "content": broadcast.content,
                })

            return Response({
                "success": True,
                "broadcasts": broadcasts_data
            }, status=HTTP_200_OK)

        except User.DoesNotExist:
            return Response({
                "success": False,
                "error": "User not found."
            }, status=HTTP_404_NOT_FOUND)


class GetBroadcastById(APIView):
    """
    获取指定 ID 的广播消息（仅管理员权限）。
    """

    def post(self, request):
        data = decode_request(request)
        user_id = data.get('user_id')
        broadcast_id = data.get('broadcast_id')

        try:
            # 获取用户信息
            user = User.objects.get(id=user_id)

            if user.user_role != 1:
                return Response({
                    "success": False,
                    "error": "权限不足",
                    "message": "权限不足"
                }, status=HTTP_400_BAD_REQUEST)

            # 获取指定的广播
            try:
                broadcast = Broadcast.objects.get(id=broadcast_id)
            except Broadcast.DoesNotExist:
                return Response({
                    "success": False,
                    "error": "Broadcast not found."
                }, status=HTTP_404_NOT_FOUND)

            # 返回广播的详细信息
            return Response({
                "success": True,
                "broadcast_details": {
                    "id": broadcast.id,
                    "sender": broadcast.sender,
                    "sent_at": broadcast.sent_at,
                    "last_updated": broadcast.last_updated,
                    "title": broadcast.title,
                    "content": broadcast.content,
                }
            }, status=HTTP_200_OK)

        except User.DoesNotExist:
            return Response({
                "success": False,
                "error": "User not found."
            }, status=HTTP_404_NOT_FOUND)
