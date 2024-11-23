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
                source=data.get('source'),
                tags=data.get('tags'),
                difficulty=data['difficulty'],
                answer=data.get('answer'),
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

        except User.DoesNotExist:
            return Response({
                'success': False,
                'error': 'User not found'
            }, status=404)


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
                defaults={
                    'is_correct': is_correct,
                    'question_subject': question.subject,  # 自动填充科目
                          }
            )

            return Response({
                "success": True,
                "message": f"Question {question_id} completed. {'Correct' if is_correct else 'Incorrect'}",
                "record_id": record.id
            }, status=HTTP_200_OK)

        except User.DoesNotExist:
            return Response({
                'success': False,
                'error': 'User not found'
            }, status=404)

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
                description=data.get('description'),
            )

            # 关联题目到题库
            question_ids = data.get('question_ids')
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

        except User.DoesNotExist:
            return Response({
                'success': False,
                'error': 'User not found'
            }, status=404)

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

        except User.DoesNotExist:
            return Response({
                'error': 'User not found'
            }, status=404)

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

        except User.DoesNotExist:
            return Response({
                'success': False,
                'error': 'User not found'
            }, status=404)

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

        except User.DoesNotExist:
            return Response({
                'success': False,
                'error': 'User not found'
            }, status=HTTP_404_NOT_FOUND)

        except Question.DoesNotExist:
            return Response({"error": "Question not found."}, status=HTTP_404_NOT_FOUND)


# 获取所有 QuestionBank
class GetAllQuestionBanks(APIView):
    def post(self, request):
        # 获取所有题库
        try:
            user_id = request.data['user_id']
            user = User.objects.get(id=user_id)

            question_banks = QuestionBank.objects.all()

            # 构造返回的数据
            question_banks_data = []
            for qb in question_banks:
                question_banks_data.append({
                    "id": qb.id,
                    "subject": qb.subject,
                    "estimated_time": qb.estimated_time,
                    "created_at": qb.created_at,
                    "creator": qb.creator.name,
                    "question_count": qb.question_count,
                })

            return Response({
                "success": True,
                "question_banks": question_banks_data
            }, status=HTTP_200_OK)

        except User.DoesNotExist:
            return Response({
                'success': False,
                'error': 'User not found'
            }, status=HTTP_404_NOT_FOUND)


# 获取所有 Question
class GetAllQuestions(APIView):
    def post(self, request):
        try:
            # 获取所有题目
            user_id = request.data['user_id']
            user = User.objects.get(id=user_id)
            questions = Question.objects.all()

            # 构造返回的数据
            questions_data = []
            for question in questions:
                questions_data.append({
                    "id": question.id,
                    "type": question.type,
                    "content": question.content,
                    "subject": question.subject,
                    "added_at": question.added_at,
                    "difficulty": question.difficulty,
                    "answer": question.answer,
                    "tags": question.tags,
                    "added_by": question.added_by.name,
                    "user_status": question.get_user_status(user)  # 获取用户对该题目的做题状态
                })

            return Response({
                "success": True,
                "questions": questions_data
            }, status=HTTP_200_OK)

        except User.DoesNotExist:
            return Response({
                'success': False,
                'error': 'User not found'
            }, status=HTTP_404_NOT_FOUND)


# 获取某一科目的所有 Question
class GetQuestionsBySubject(APIView):
    def post(self, request):
        try:
            # 获取某一科目的所有题目
            user_id = request.data['user_id']
            user = User.objects.get(id=user_id)
            subject = request.data['subject']
            questions = Question.objects.filter(subject=subject)

            # 如果没有找到该科目的题目
            if not questions:
                return Response({
                    "error": "No questions found for the given subject."
                }, status=HTTP_404_NOT_FOUND)

            # 构造返回的数据
            questions_data = []
            for question in questions:
                questions_data.append({
                    "id": question.id,
                    "type": question.type,
                    "content": question.content,
                    "subject": question.subject,
                    "added_at": question.added_at,
                    "difficulty": question.difficulty,
                    "answer": question.answer,
                    "tags": question.tags,
                    "added_by": question.added_by.name,
                    "user_status": question.get_user_status(user)  # 获取用户对该题目的做题状态
                })

            return Response({
                "success": True,
                "questions": questions_data
            }, status=HTTP_200_OK)

        except User.DoesNotExist:
            return Response({
                'success': False,
                'error': 'User not found'
            }, status=HTTP_404_NOT_FOUND)


# 获取某一科目的所有 QuestionBank
class GetQuestionBanksBySubject(APIView):
    def post(self, request):
        try:
            subject = request.data['subject']
            # 获取某一科目的所有题库
            question_banks = QuestionBank.objects.filter(subject=subject)

            # 如果没有找到该科目的题库
            if not question_banks:
                return Response({
                    "error": "No question banks found for the given subject."
                }, status=HTTP_404_NOT_FOUND)

            # 构造返回的数据
            question_banks_data = []
            for qb in question_banks:
                question_banks_data.append({
                    "id": qb.id,
                    "subject": qb.subject,
                    "estimated_time": qb.estimated_time,
                    "created_at": qb.created_at,
                    "creator": qb.creator.name,
                    "question_count": qb.question_count
                })

            return Response({
                "success": True,
                "question_banks": question_banks_data
            }, status=HTTP_200_OK)

        except User.DoesNotExist:
            return Response({
                'success': False,
                'error': 'User not found'
            }, status=HTTP_404_NOT_FOUND)

        except QuestionBank.DoesNotExist:
            return Response({"error": "QuestionBank not found."}, status=HTTP_404_NOT_FOUND)


# 获取某一 QuestionBank 内的所有 Question
class GetQuestionsByQuestionBank(APIView):
    def post(self, request):
        try:
            # 获取指定题库
            user_id = request.data['user_id']
            user = User.objects.get(id=user_id)
            question_bank_id = request.data['question_bank_id']
            question_bank = QuestionBank.objects.get(id=question_bank_id)

            # 获取该题库内所有的题目
            questions = question_bank.questions.all()

            # 构造返回的数据
            # 初始化返回数据
            questions_data = []

            # 遍历题目类型并按类型获取题目 ID
            for question_type, type_label in Question.TYPE_CHOICES:
                questions = question_bank.questions.filter(type=question_type).order_by("id")

                # 如果该类型的题目存在，添加到结果
                if questions.exists():
                    questions_data.append({
                        "type": type_label,
                        "questions": [
                            {
                                "id": question.id,
                                "user_status": question.get_user_status(user)  # 用户是否已作答
                            }
                            for question in questions
                        ]
                    })

            return Response({
                "success": True,
                "questions": questions_data
            }, status=HTTP_200_OK)

        except User.DoesNotExist:
            return Response({
                'success': False,
                'error': 'User not found'
            }, status=HTTP_404_NOT_FOUND)

        except QuestionBank.DoesNotExist:
            return Response({"error": "QuestionBank not found."}, status=HTTP_404_NOT_FOUND)


# 获取某一特定 id 的 Question 详细信息
class GetQuestionById(APIView):
    def post(self, request):
        try:
            # 获取指定题目
            user_id = request.data['user_id']
            user = User.objects.get(id=user_id)
            question_id = request.data['question_id']
            question = Question.objects.get(id=question_id)

            # 构造返回的数据
            question_data = {
                "id": question.id,
                "type": question.type,
                "content": question.content,
                "subject": question.subject,
                "added_at": question.added_at,
                "difficulty": question.difficulty,
                "answer": question.answer,
                "tags": question.tags,
                "added_by": question.added_by.username,
                "user_status": question.get_user_status(user)  # 获取用户对该题目的做题状态
            }

            return Response({
                "success": True,
                "question": question_data
            }, status=HTTP_200_OK)

        except User.DoesNotExist:
            return Response({
                'success': False,
                'error': 'User not found'
            }, status=HTTP_404_NOT_FOUND)

        except Question.DoesNotExist:
            return Response({"error": "Question not found."}, status=HTTP_404_NOT_FOUND)
