from django.shortcuts import render
from django.utils.timezone import now, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from discussions.models import Discussion, Reply
from users.models import User
from utils.views import decode_request

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.permissions import AllowAny

@method_decorator(csrf_exempt, name='dispatch')
class CreateDiscussion(APIView):
    def post(self, request):
        try:
            data = decode_request(request)
            user_id = data.get('user_id')
            user = User.objects.get(student_id=user_id)
            print(user)
            title = data.get('title')
            content = data.get('content')
            tag = data.get('tag')
            avatar = user.avatar

            if not title or not content:
                return Response({"error": "Title and content are required."}, status=HTTP_400_BAD_REQUEST)

            discussion = Discussion.objects.create(
                title=title,
                content=content,
                publisher=user,
                avatar=avatar,
                tag=tag,
            )
            return Response({"success": True, "discussion_id": discussion.id}, status=HTTP_200_OK)


        except User.DoesNotExist:
            return Response({
                'success': False,
                'error': 'User not found'
            }, status=HTTP_404_NOT_FOUND)


class LikePost(APIView):
    def post(self, request):
        data = decode_request(request)
        user_id = data.get('user_id')
        user = User.objects.get(student_id=user_id)
        discussion_id = data.get('dis_id')
        try:
            discussion = Discussion.objects.get(id=discussion_id)
            if user in discussion.likes.all():
                discussion.likes.remove(user)  # 取消点赞
                liked = False
            else:
                discussion.likes.add(user)  # 点赞
                liked = True

            return Response({"success": True, "liked": liked, "like_count": discussion.likes.count()},
                            status=HTTP_200_OK)
        except User.DoesNotExist:
            return Response({
                'success': False,
                'error': 'User not found'
            }, status=HTTP_404_NOT_FOUND)

        except Discussion.DoesNotExist:
            return Response({"error": "Discussion not found."}, status=HTTP_404_NOT_FOUND)

class MarkDiscussion(APIView):
    def post(self, request):
        data = decode_request(request)
        user_id = data.get('user_id')
        user = User.objects.get(student_id=user_id)
        discussion_id = data.get('dis_id')
        try:
            discussion = Discussion.objects.get(id=discussion_id)
            
            discussion.isMarked = not discussion.isMarked
            discussion.save()
            return Response({"success": True},status=HTTP_200_OK)
        except User.DoesNotExist:
            return Response({
                'success': False,
                'error': 'User not found'
            }, status=HTTP_404_NOT_FOUND)

        except Discussion.DoesNotExist:
            return Response({"error": "Discussion not found."}, status=HTTP_404_NOT_FOUND)
        
class LikeReply(APIView):
    def post(self, request):
        data = decode_request(request)
        user_id = data.get('user_id')
        user = User.objects.get(student_id=user_id)
        reply_id = data.get('dis_id')
        try:
            discussion = Reply.objects.get(id=reply_id)
            if user in discussion.likes.all():
                discussion.likes.remove(user)  # 取消点赞
                liked = False
            else:
                discussion.likes.add(user)  # 点赞
                liked = True

            return Response({"success": True, "liked": liked, "like_count": discussion.likes.count()},
                            status=HTTP_200_OK)
        except User.DoesNotExist:
            return Response({
                'success': False,
                'error': 'User not found'
            }, status=HTTP_404_NOT_FOUND)

        except Reply.DoesNotExist:
            return Response({"error": "Reply not found."}, status=HTTP_404_NOT_FOUND)


class SubscribeDiscussion(APIView):
    def post(self, request):
        data = decode_request(request)
        user_id = data.get('user_id')
        user = User.objects.get(student_id=user_id)
        discussion_id = data.get('dis_id')
        try:
            discussion = Discussion.objects.get(id=discussion_id)
            if user in discussion.subscribers.all():
                discussion.subscribers.remove(user)  # 取消订阅
                subscribed = False
            else:
                discussion.subscribers.add(user)  # 订阅
                subscribed = True

            return Response({"success": True, "subscribed": subscribed}, status=HTTP_200_OK)

        except User.DoesNotExist:
            return Response({
                'success': False,
                'error': 'User not found'
            }, status=HTTP_404_NOT_FOUND)

        except Discussion.DoesNotExist:
            return Response({"error": "Discussion not found."}, status=HTTP_404_NOT_FOUND)


class CreateReply(APIView):
    def post(self, request):
        data = decode_request(request)
        user_id = data.get("user_id")
        user = User.objects.get(student_id=user_id)
        discussion_id = data.get("discussion_id")
        content = data.get("content")
        
        if not content:
            return Response({"error": "Content is required."}, status=HTTP_400_BAD_REQUEST)

        try:
            # 获取主帖
            discussion = Discussion.objects.get(id=discussion_id)

            # 创建回复
            reply = Reply.objects.create(
                discussion=discussion,
                content=content,
                publisher=user,
                avatar=user.avatar,
            )

            # 更新主帖的最后更新时间
            discussion.last_updated = now()
            discussion.save()

            # 通知主帖发布者有新回复
            reply.notify_publisher()

            # 通知订阅者帖子更新
            update_content = f"新回复by{user.name}：{content[:50]}..."  # 节选回复内容
            discussion.notify_subscribers(update_content)

            return Response({"success": True, "reply_id": reply.id}, status=HTTP_200_OK)

        except User.DoesNotExist:
            return Response({
                'success': False,
                'error': 'User not found'
            }, status=HTTP_404_NOT_FOUND)

        except Discussion.DoesNotExist:
            return Response({"error": "Discussion not found."}, status=HTTP_404_NOT_FOUND)


class EditDiscussion(APIView):
    def post(self, request):
        data = decode_request(request)
        user_id = data.get("user_id")
        user = User.objects.get(student_id=user_id)
        discussion_id = data.get("discussion_id")
        content = data.get("content")
        if not content:
            return Response({"error": "Content is required."}, status=HTTP_400_BAD_REQUEST)

        try:
            # 获取主帖
            discussion = Discussion.objects.get(id=discussion_id)

            # 检查编辑权限
            if discussion.publisher != user:
                return Response({"error": "You do not have permission to edit this discussion."},
                                status=HTTP_400_BAD_REQUEST)

            # 更新帖子内容
            discussion.content = content
            discussion.last_updated = now()  # 更新最后更新时间
            discussion.save()

            # 通知订阅者帖子更新
            update_content = f"帖子内容更新: {content[:50]}..."
            discussion.notify_subscribers(update_content)

            return Response({"success": True, "message": "Discussion updated successfully."}, status=HTTP_200_OK)

        except User.DoesNotExist:
            return Response({
                'success': False,
                'error': 'User not found'
            }, status=HTTP_404_NOT_FOUND)

        except Discussion.DoesNotExist:
            return Response({"error": "Discussion not found."}, status=HTTP_404_NOT_FOUND)


class EditReply(APIView):
    def post(self, request):
        data = decode_request(request)
        user_id = data.get("user_id")
        user = User.objects.get(student_id=user_id)
        reply_id = data.get("discussion_id")
        content = data.get("content")

        if not content:
            return Response({"error": "Content is required."}, status=HTTP_400_BAD_REQUEST)

        try:
            # 获取回复
            reply = Reply.objects.get(id=reply_id)

            # 检查编辑权限
            if reply.publisher != user:
                return Response({"error": "You do not have permission to edit this reply."},
                                status=HTTP_400_BAD_REQUEST)

            # 更新回复内容
            reply.content = content
            reply.last_updated = now()  # 更新最后更新时间
            reply.save()

            # 更新主帖状态
            discussion = reply.discussion
            discussion.last_updated = now()  # 主帖最后更新时间同步更新
            discussion.save()

            # 通知订阅者帖子更新
            update_content = f"回复内容更新: {content[:50]}..."
            discussion.notify_subscribers(update_content)

            return Response({"success": True, "message": "Reply updated successfully."}, status=HTTP_200_OK)

        except User.DoesNotExist:
            return Response({
                'success': False,
                'error': 'User not found'
            }, status=HTTP_404_NOT_FOUND)

        except Discussion.DoesNotExist:
            return Response({"error": "Discussion not found."}, status=HTTP_404_NOT_FOUND)

        except Reply.DoesNotExist:
            return Response({"error": "Reply not found."}, status=HTTP_404_NOT_FOUND)


class GetAllDiscussions(APIView):
    def post(self, request):
        data = decode_request(request)

        # 获取筛选条件
        tag = data.get('tag')
        time_range = data.get('time_range')  # 可能的值: "7d", "1m", "6m", "1y"

        # 基本查询
        discussions = Discussion.objects.all()
        # 按更新时间排序
        discussions = discussions.order_by("-last_updated")

        # 构造返回数据
        discussions_data = []
        for discussion in discussions:
            discussions_data.append({
                "id": discussion.id,
                "title": discussion.title,
                "publisher": discussion.publisher.name,
                "avatar": discussion.avatar,
                "publishTime": discussion.publish_time,
                "lastUpdated": discussion.last_updated,
                "tag": discussion.tag,
                "isMarked": discussion.isMarked,
                "summary": discussion.content[:100]  # 摘要显示内容前100字符
            })

        return Response({
            "success": True,
            "discussions": discussions_data
        }, status=HTTP_200_OK)


class GetDiscussionReplies(APIView):
    def post(self, request):
        data = decode_request(request)
        user_id = data.get("user_id")
        user = User.objects.get(student_id=user_id)
        discussion_id = data.get('discussion_id')

        try:
            # 获取讨论帖
            discussion = Discussion.objects.get(id=discussion_id)

            # 获取该讨论帖的所有回复
            replies = discussion.replies.all().order_by("publish_time")

            # 构造返回数据
            replies_data = []
            for reply in replies:
                replies_data.append({
                    "id": reply.id,
                    "publisher": reply.publisher.name,
                    "avatar": reply.avatar,
                    "publishTime": reply.publish_time,
                    "lastUpdated": reply.last_updated,
                    "content": reply.content,
                    "isLiked": reply.likes.filter(id=user_id).exists()  # 当前用户是否点赞
                })

            return Response({
                "success": True,
                "replies": replies_data
            }, status=HTTP_200_OK)

        except User.DoesNotExist:
            return Response({
                'success': False,
                'error': 'User not found'
            }, status=HTTP_404_NOT_FOUND)

        except Discussion.DoesNotExist:
            return Response({"error": "Discussion not found."}, status=HTTP_404_NOT_FOUND)

@method_decorator(csrf_exempt, name='dispatch')
class GetDiscussionById(APIView):
    def post(self, request):
        data = decode_request(request)
        user_id = data.get("user_id")
        discussion_id = data.get("dis_id")
        try:
            # 获取主帖
            discussion = Discussion.objects.get(id=discussion_id)

            # 获取所有回复
            replies = discussion.replies.all().order_by("publish_time")
            replies_data = []
            for reply in replies:
                replies_data.append({
                    "id": reply.id,
                    "publisher": reply.publisher.name,
                    "publisherId": reply.publisher.student_id,
                    "avatar": reply.avatar,
                    "publishTime": reply.publish_time,
                    "lastUpdated": reply.last_updated,
                    "content": reply.content,
                    "isLiked": reply.likes.filter(student_id=user_id).exists()  # 当前用户是否点赞
                })
            # 构造主帖数据
            discussion_data = {
                "id": discussion.id,
                "title": discussion.title,
                "publisher": discussion.publisher.name,
                "publisherId": discussion.publisher.student_id,
                "avatar": discussion.avatar,
                "publishTime": discussion.publish_time,
                "lastUpdated": discussion.last_updated,
                "tag": discussion.tag,
                "isMarked": discussion.isMarked,
                "content": discussion.content,
                "isLiked": discussion.likes.filter(student_id=user_id).exists(),  # 当前用户是否点赞
                "isSubscribed": discussion.subscribers.filter(student_id=user_id).exists(),  # 当前用户是否已订阅
            }

            return Response({
                "success": True,
                "discussion": discussion_data,
                "replies": replies_data  # 回复列表
            }, status=HTTP_200_OK)

        except Discussion.DoesNotExist:
            return Response({"error": "Discussion not found."}, status=HTTP_404_NOT_FOUND)

        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=HTTP_404_NOT_FOUND)
@method_decorator(csrf_exempt, name='dispatch')
class DeleteDiscussion(APIView):
    """
    删除指定 ID 的讨论帖，仅允许管理员或讨论帖的发布者删除。
    """
    def post(self, request):
        try:
            data = decode_request(request)
            user_id = data.get("user_id")
            discussion_id = data.get("discussion_id")
            user = User.objects.get(student_id=user_id)
            discussion = Discussion.objects.get(id=discussion_id)
            # 权限检查：必须是管理员或讨论发布者
            if user.user_role != 1 and discussion.publisher != user:
                return Response({
                    "success": False,
                    "error": "You do not have permission to delete this discussion."
                }, status=HTTP_400_BAD_REQUEST)

            # 删除讨论
            discussion.delete()
            return Response({
                "success": True,
                "message": f"Discussion {discussion_id} deleted successfully."
            }, status=HTTP_200_OK)

        except Discussion.DoesNotExist:
            return Response({"error": "Discussion not found."}, status=HTTP_404_NOT_FOUND)

        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=HTTP_404_NOT_FOUND)

        except KeyError as e:
            return Response({"error": f"Missing required field: {str(e)}"}, status=HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class DeleteReply(APIView):
    """
    删除指定 ID 的回复，仅允许管理员或回复的发布者删除。
    """

    def post(self, request):
        try:
            data = decode_request(request)
            user_id = data.get("user_id")
            reply_id = data.get("discussion_id")
            user = User.objects.get(student_id=user_id)
            reply = Reply.objects.get(id=reply_id)

            # 权限检查：必须是管理员或回复发布者
            if user.user_role != 1 and reply.publisher != user:
                return Response({
                    "success": False,
                    "error": "You do not have permission to delete this reply."
                }, status=HTTP_400_BAD_REQUEST)

            # 删除回复
            reply.delete()
            return Response({
                "success": True,
                "message": f"Reply {reply_id} deleted successfully."
            }, status=HTTP_200_OK)

        except Reply.DoesNotExist:
            return Response({"error": "Reply not found."}, status=HTTP_404_NOT_FOUND)

        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=HTTP_404_NOT_FOUND)

        except KeyError as e:
            return Response({"error": f"Missing required field: {str(e)}"}, status=HTTP_400_BAD_REQUEST)