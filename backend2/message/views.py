from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response
from rest_framework.views import APIView

from message.models import Message
from users.models import User


# Create your views here.

class GetAllMessage(APIView):
    def post(self, request):
        try:
            user_id = request.data['user_id']
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


class MarkMessageAsRead(APIView):
    def post(self, request):
        try:
            user_id = request.data['user_id']
            message_id = request.data['message_id']

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
