from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from .models import Broadcast


class PublishBroadcast(APIView):
    """
    发布新的广播消息。
    """

    def post(self, request):
        try:
            sender = request.data.get("sender", "系统通知")  # 默认发件人名字为"系统通知"
            content = request.data["content"]

            # 创建新的广播消息
            broadcast = Broadcast.objects.create(sender=sender, content=content)

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

        except KeyError:
            return Response({
                "success": False,
                "error": "Missing required field: 'content'."
            }, status=HTTP_400_BAD_REQUEST)
