from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response
from rest_framework.views import APIView

from message.models import Message
from users.models import User
from utils.views import decode_request


# Create your views here.
# 
# 这里是未读消息
class GetAllMessage(APIView):
    def post(self, request):
        try:
            data = decode_request(request)
            user_id = data.get('user_id')
            user = User.objects.get(id=user_id)

            # 获取用户作为发件人或收件人的消息
            received_messages = Message.objects.filter(receiver=user, is_read=False)

            all_messages = received_messages.order_by('-sent_at')  # 按发送时间倒序排列

            messages_data = [
                {
                    'id': message.id,
                    'sender': message.sender.id,
                    'receiver': message.receiver.id,
                    'content': message.content,
                    'is_read': message.is_read,
                    'sent_at': message.sent_at,
                    'sender_avatar': message.sender_avatar,
                }
                for message in all_messages
            ]

            return Response({
                'message': "success",
                'messages': messages_data
            }, status=HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

# 获取所有已读消息
class GetAllReadMessages(APIView):
    """
    获取所有已读消息
    """

    def post(self, request):
        try:
            data = decode_request(request)
            user_id = data.get('user_id')
            user = User.objects.get(id=user_id)

            # 获取用户作为收件人的已读消息
            read_messages = Message.objects.filter(receiver=user, is_read=True)

            # 按发送时间倒序排列
            all_read_messages = read_messages.order_by('-sent_at')

            # 构造返回数据
            messages_data = [
                {
                    'id': message.id,
                    'sender': message.sender.id,
                    'receiver': message.receiver.id,
                    'content': message.content,
                    'is_read': message.is_read,
                    'sent_at': message.sent_at,
                    'sender_avatar': message.sender_avatar,
                }
                for message in all_read_messages
            ]

            return Response({
                'message': "success",
                'messages': messages_data
            }, status=HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)


class MarkMessageAsRead(APIView):
    def post(self, request):
        try:
            data = decode_request(request)
            user_id = data.get('user_id')
            message_id = data.get('message_id')

            # 获取用户和消息
            user = User.objects.get(id=user_id)
            message = Message.objects.get(id=message_id)

            # 标记为已读
            message.is_read = True
            message.save()

            return Response({'success': f'Message {message_id} marked as read.'}, status=HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

        except Message.DoesNotExist:
            return Response({'error': 'Message not found'}, status=404)


class MarkMessageAsUnread(APIView):
    def post(self, request):
        try:
            data = decode_request(request)
            user_id = data.get('user_id')
            message_id = data.get('message_id')

            # 获取用户和消息
            user = User.objects.get(id=user_id)
            message = Message.objects.get(id=message_id)

            # 检查是否是接收者
            if message.receiver != user:
                return Response({'error': 'Permission denied'}, status=HTTP_400_BAD_REQUEST)

            # 标记为未读
            message.is_read = False
            message.save()

            return Response({'success': f'Message {message_id} marked as unread.'}, status=HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

        except Message.DoesNotExist:
            return Response({'error': 'Message not found'}, status=404)


class MarkAllMessagesAsRead(APIView):
    def post(self, request):
        try:
            data = decode_request(request)
            user_id = data.get('user_id')
            user = User.objects.get(id=user_id)

            # 获取用户收到的所有未读消息
            unread_messages = Message.objects.filter(receiver=user, is_read=False)

            # 将所有消息标记为已读
            unread_messages.update(is_read=True)

            return Response({
                'success': True,
                'message': 'All messages marked as read.'
            }, status=HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)


class SendMessage(APIView):
    def post(self, request):
        try:
            sender_id = request.data['sender_id']
            receiver_id = request.data['receiver_id']
            content = request.data['content']
            # sender_avatar = request.data.get('sender_avatar', '')  # 可选参数，发件人头像

            # 获取发送者和接收者
            sender = User.objects.get(id=sender_id)
            receiver = User.objects.get(id=receiver_id)
            sender_avatar = sender.avatar

            # 创建新消息
            new_message = Message.objects.create(
                sender=sender,
                receiver=receiver,
                content=content,
                sender_avatar=sender_avatar,
                is_read=False  # 默认消息未读
            )

            # 返回成功响应
            return Response({
                'success': 'Message sent successfully.',
                'message_id': new_message.id
            }, status=HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'error': 'Sender or Receiver not found'}, status=404)


# https://randomuser.me/api/portraits/men/85.jpg

class SendSystemMessage(APIView):
    def post(self, request):
        try:
            # sender_id = request.data['sender_id']
            receiver_id = request.data['receiver_id']
            content = request.data['content']
            # sender_avatar = request.data.get('sender_avatar', '')  # 可选参数，发件人头像

            # 获取发送者和接收者
            # sender = User.objects.get(id=sender_id)
            receiver = User.objects.get(id=receiver_id)
            sender_avatar = "https://randomuser.me/api/portraits/men/85.jpg"

            # 创建新消息
            new_message = Message.objects.create(
                sender=None,
                receiver=receiver,
                content=content,
                sender_avatar=sender_avatar,
                is_read=False  # 默认消息未读
            )

            # 返回成功响应
            return Response({
                'success': 'Message sent successfully.',
                'message_id': new_message.id
            }, status=HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'error': 'Sender or Receiver not found'}, status=404)
