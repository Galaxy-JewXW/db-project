from datetime import datetime

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from learingCompanionInBeihang.apps.users.models import User
from .models import Question, QuestionBank, UserQuestionRecord, QuestionDiscussion, QuestionComment
from rest_framework.permissions import IsAuthenticated


# 用户上传 Question
class UploadQuestion(APIView):
    def post(self, request):
        try:
            user_id = request.data['user_id']
            data = request.data['data']
            user = User.objects.get(id=user_id)

            # 创建 Question
            question = Question.objects.create(
                type=data['type'],
                content=data['content'],
                subject=data['subject'],
                added_at=data['added_at'],
                source=data.get('source', "用户上传"),
                tags=data.get('tags', []),
                difficulty=data['difficulty'],
                answer=data.get('answer', None),
                added_by=user
            )

            QuestionDiscussion.objects.create(
                question=question,
                created_by=user,
                content=f"这是题目 {question.id} 的默认讨论区。"
            )

            return Response({
                "success": True,
                "message": "Question uploaded successfully.",
                "question_id": question.id
            }, status=HTTP_200_OK)

        except KeyError as e:
            return Response({
                "success": False,
                "error": f"Missing required field: {str(e)}"
            }, status=HTTP_400_BAD_REQUEST)


# 用户完成题目
class CompleteQuestion(APIView):
    def post(self, request):
        try:
            user_id = request.data['user_id']
            user = User.objects.get(id=user_id)
            question_id = request.data['question_id']
            is_correct = request.data['is_correct']

            # 获取 Question
            question = Question.objects.get(id=question_id)

            # 创建或更新做题记录
            record, created = UserQuestionRecord.objects.update_or_create(
                user=user,
                question=question,
                defaults={'is_correct': is_correct}
            )

            return Response({
                "success": True,
                "message": f"Question {question_id} completed. {'Correct' if is_correct else 'Incorrect'}",
                "record_id": record.id
            }, status=HTTP_200_OK)

        except Question.DoesNotExist:
            return Response({
                "success": False,
                "error": "Question not found."
            }, status=HTTP_404_NOT_FOUND)

        except KeyError as e:
            return Response({
                "success": False,
                "error": f"Missing required field: {str(e)}"
            }, status=HTTP_400_BAD_REQUEST)


# 创建 QuestionBank
class CreateQuestionBank(APIView):
    def post(self, request):
        try:
            user_id = request.data['user_id']
            data = request.data['data']
            user = User.objects.get(id=user_id)

            # 创建 QuestionBank
            question_bank = QuestionBank.objects.create(
                subject=data['subject'],
                estimated_time=data['estimated_time'],
                creator=user,
                description=data.get('description', ""),
            )

            # 关联题目到题库
            question_ids = data.get('question_ids', [])
            questions = Question.objects.filter(id__in=question_ids)
            question_bank.questions.add(*questions)

            # 更新题目数量
            question_bank.question_count = question_bank.questions.count()
            question_bank.save()

            return Response({
                "success": True,
                "message": "QuestionBank created successfully.",
                "question_bank_id": question_bank.id
            }, status=HTTP_200_OK)

        except KeyError as e:
            return Response({
                "success": False,
                "error": f"Missing required field: {str(e)}"
            }, status=HTTP_400_BAD_REQUEST)


class AddComment(APIView):
    def post(self, request):
        try:
            question_id = request.data['question_id']
            content = request.data['content']
            user_id = request.data['user_id']
            user = User.objects.get(id=user_id)

            # 获取题目及其讨论区
            question = Question.objects.get(id=question_id)
            discussion = question.discussion

            # 创建评论
            comment = QuestionComment.objects.create(
                discussion=discussion,
                created_by=user,
                creator_avatar=user.avatar,
                content=content
            )

            return Response({
                "success": True,
                "message": "QuestionComment added successfully.",
                "comment_id": comment.id
            }, status=HTTP_200_OK)

        except Question.DoesNotExist:
            return Response({"error": "Question not found."}, status=HTTP_404_NOT_FOUND)

        except KeyError as e:
            return Response({"error": f"Missing required field: {str(e)}"}, status=HTTP_400_BAD_REQUEST)


class LikeComment(APIView):
    def post(self, request):
        try:
            comment_id = request.data['comment_id']
            user_id = request.data['user_id']
            user = User.objects.get(id=user_id)

            # 获取评论
            comment = QuestionComment.objects.get(id=comment_id)

            # 点赞操作
            if user in comment.likes.all():
                comment.likes.remove(user)  # 取消点赞
                liked = False
            else:
                comment.likes.add(user)  # 添加点赞
                liked = True

            return Response({
                "success": True,
                "liked": liked,
                "like_count": comment.like_count()
            }, status=HTTP_200_OK)

        except QuestionComment.DoesNotExist:
            return Response({"error": "QuestionComment not found."}, status=HTTP_404_NOT_FOUND)

        except KeyError:
            return Response({"error": "comment_id is required."}, status=HTTP_400_BAD_REQUEST)


class GetQuestionComments(APIView):
    def post(self, request):
        try:
            user_id = request.data['user_id']
            user = User.objects.get(id=user_id)
            question_id = request.data['question_id']

            # 获取题目及其讨论区
            question = Question.objects.get(id=question_id)
            discussion = question.discussion

            # 获取所有评论
            comments = discussion.comments.all().order_by('-created_at')

            # 构造评论数据
            comments_data = []
            for comment in comments:
                comments_data.append({
                    "id": comment.id,
                    "content": comment.content,
                    "created_by": comment.created_by.name,
                    "creator_avatar": comment.creator_avatar,
                    "created_at": comment.created_at,
                    "like_count": comment.like_count(),
                    "liked_by_user": user in comment.likes.all()  # 判断用户是否点赞
                })

            return Response({
                "success": True,
                "comments": comments_data
            }, status=HTTP_200_OK)

        except Question.DoesNotExist:
            return Response({"error": "Question not found."}, status=HTTP_404_NOT_FOUND)
