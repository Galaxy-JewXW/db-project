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
                added_by=user,
                option_count=data.get('option_count', 0)  # 允许前端指定选项数量
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
                    "option_count": question.option_count,  # 新增选项数量
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
                    "option_count": question.option_count,  # 新增选项数量
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
            return Response({'success': False, "error": "QuestionBank not found."}, status=HTTP_404_NOT_FOUND)


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
                "added_by": question.added_by.name,
                "option_count": question.option_count,  # 新增选项数量
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
            return Response({'success': False, "error": "Question not found."}, status=HTTP_404_NOT_FOUND)


class DeleteQuestion(APIView):
    """
    删除题目。
    """

    def post(self, request):
        try:
            user_id = request.data['user_id']
            user = User.objects.get(id=user_id)

            if user.user_role != 1:  # 检查是否为管理员/老师
                return Response({
                    "success": False,
                    "error": "权限不足",
                    "message": "只有管理员或老师可以删除题目。"
                }, status=HTTP_400_BAD_REQUEST)

            question_id = request.data['question_id']

            # 获取题目
            question = Question.objects.get(id=question_id)
            question.delete()

            return Response({
                "success": True,
                "message": "题目删除成功。",
                "question_id": question_id
            }, status=HTTP_200_OK)

        except User.DoesNotExist:
            return Response({
                'success': False,
                'error': '用户未找到。'
            }, status=HTTP_404_NOT_FOUND)

        except Question.DoesNotExist:
            return Response({
                "success": False,
                "error": "题目未找到。"
            }, status=HTTP_404_NOT_FOUND)

        except KeyError as e:
            return Response({
                "success": False,
                "error": f"缺少必要字段: {str(e)}"
            }, status=HTTP_400_BAD_REQUEST)


class GetQuestionBankById(APIView):
    """
    获取指定 QuestionBank 的详细信息及其包含的所有题目。
    """

    def post(self, request):
        try:
            # 获取请求数据
            user_id = request.data['user_id']
            question_bank_id = request.data['question_bank_id']
            user = User.objects.get(id=user_id)
            question_bank = QuestionBank.objects.get(id=question_bank_id)

            # 获取该题库中的所有题目
            questions_data = []

            for question_type, type_label in Question.TYPE_CHOICES:
                questions = question_bank.questions.filter(type=question_type).order_by("id")
                if questions.exists():
                    questions_data.append({
                        "type": type_label,
                        "questions": [
                            {
                                "id": question.id,
                                "content": question.content,
                                "subject": question.subject,
                                "difficulty": question.difficulty,
                                "option_count": question.option_count,  # 包含选项数量
                                "user_status": question.get_user_status(user)  # 获取用户是否已作答
                            }
                            for question in questions
                        ]
                    })

            # 构造返回的题库数据
            question_bank_data = {
                "id": question_bank.id,
                "subject": question_bank.subject,
                "estimated_time": question_bank.estimated_time,
                "created_at": question_bank.created_at,
                "creator": question_bank.creator.name,
                "description": question_bank.description,
                "question_count": question_bank.question_count,
                "questions": questions_data  # 按题目类型分类的题目列表
            }

            return Response({
                "success": True,
                "question_bank": question_bank_data
            }, status=HTTP_200_OK)

        except User.DoesNotExist:
            return Response({
                "success": False,
                "error": "User not found."
            }, status=HTTP_404_NOT_FOUND)

        except QuestionBank.DoesNotExist:
            return Response({
                "success": False,
                "error": "QuestionBank not found."
            }, status=HTTP_404_NOT_FOUND)

        except KeyError as e:
            return Response({
                "success": False,
                "error": f"Missing required field: {str(e)}"
            }, status=HTTP_400_BAD_REQUEST)


class DeleteQuestionBank(APIView):
    """
    删除题库的视图函数，仅允许管理员或题库创建者删除。
    """

    def post(self, request):
        try:
            # 获取请求数据
            user_id = request.data['user_id']
            question_bank_id = request.data['question_bank_id']
            user = User.objects.get(id=user_id)

            # 检查权限：是否为管理员
            if user.user_role != 1:
                return Response({
                    "success": False,
                    "error": "权限不足",
                    "message": "只有管理员可以删除题库。"
                }, status=HTTP_400_BAD_REQUEST)

            # 获取题库
            try:
                question_bank = QuestionBank.objects.get(id=question_bank_id)
            except QuestionBank.DoesNotExist:
                return Response({
                    "success": False,
                    "error": "题库未找到。"
                }, status=HTTP_404_NOT_FOUND)

            # 确保只有题库创建者或其他管理员可以删除题库
            if question_bank.creator != user and user.user_role != 1:
                return Response({
                    "success": False,
                    "error": "权限不足",
                    "message": "只有题库创建者或管理员可以删除题库。"
                }, status=HTTP_400_BAD_REQUEST)

            # 删除题库
            question_bank.delete()
            return Response({
                "success": True,
                "message": f"题库 {question_bank_id} 删除成功。"
            }, status=HTTP_200_OK)

        except User.DoesNotExist:
            return Response({
                "success": False,
                "error": "用户未找到。"
            }, status=HTTP_404_NOT_FOUND)

        except KeyError as e:
            return Response({
                "success": False,
                "error": f"缺少必要字段: {str(e)}"
            }, status=HTTP_400_BAD_REQUEST)


class EditQuestion(APIView):
    def post(self, request):
        try:
            user_id = request.data['user_id']
            question_id = request.data['question_id']
            question_data = request.data['data']

            user = User.objects.get(id=user_id)
            question = Question.objects.get(id=question_id)

            if user.user_role != 1:  # 权限检查
                return Response({"error": "Only admins or teachers can edit questions."}, status=HTTP_400_BAD_REQUEST)

            # 更新字段
            question.type = question_data['type']
            question.content = question_data['content']
            question.subject = question_data['subject']
            question.added_at = question_data['added_at']
            question.source = question_data.get('source', None)
            question.tags = question_data.get('tags', [])
            question.difficulty = question_data['difficulty']
            question.answer = question_data.get('answer', None)
            question.option_count = question_data.get('option_count', 0)  # 默认选项数量为 0

            question.save()

            return Response({
                "success": True,
                "message": f"Question {question_id} updated successfully."
            }, status=HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=HTTP_404_NOT_FOUND)

        except Question.DoesNotExist:
            return Response({"error": "Question not found."}, status=HTTP_404_NOT_FOUND)

        except KeyError as e:
            return Response({"error": f"Missing required field: {str(e)}"}, status=HTTP_400_BAD_REQUEST)


class EditQuestionInBank(APIView):
    def post(self, request):
        try:
            user_id = request.data['user_id']
            question_bank_id = request.data['question_bank_id']
            question_id = request.data['question_id']
            question_data = request.data['data']

            user = User.objects.get(id=user_id)
            question_bank = QuestionBank.objects.get(id=question_bank_id)
            question = Question.objects.get(id=question_id)

            if user.user_role != 1:  # 权限检查
                return Response({"error": "Only admins or teachers can edit questions."}, status=HTTP_400_BAD_REQUEST)

            if question not in question_bank.questions.all():
                return Response({"error": "Question does not belong to this QuestionBank."},
                                status=HTTP_400_BAD_REQUEST)

            # 更新字段
            question.type = question_data['type']
            question.content = question_data['content']
            question.subject = question_data['subject']
            question.added_at = question_data['added_at']
            question.source = question_data.get('source', None)
            question.tags = question_data.get('tags', [])
            question.difficulty = question_data['difficulty']
            question.answer = question_data.get('answer', None)
            question.option_count = question_data.get('option_count', 0)  # 默认选项数量为 0

            question.save()

            return Response({
                "success": True,
                "message": f"Question {question_id} in QuestionBank {question_bank_id} updated successfully."
            }, status=HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=HTTP_404_NOT_FOUND)

        except QuestionBank.DoesNotExist:
            return Response({"error": "QuestionBank not found."}, status=HTTP_404_NOT_FOUND)

        except Question.DoesNotExist:
            return Response({"error": "Question not found."}, status=HTTP_404_NOT_FOUND)

        except KeyError as e:
            return Response({"error": f"Missing required field: {str(e)}"}, status=HTTP_400_BAD_REQUEST)


class AddQuestionToBank(APIView):
    def post(self, request):
        try:
            user_id = request.data['user_id']
            question_bank_id = request.data['question_bank_id']
            question_id = request.data['question_id']

            user = User.objects.get(id=user_id)
            question_bank = QuestionBank.objects.get(id=question_bank_id)
            question = Question.objects.get(id=question_id)

            if user.user_role != 1:  # 权限检查
                return Response({"error": "Only admins or teachers can add questions to a QuestionBank."},
                                status=HTTP_400_BAD_REQUEST)

            # 添加题目到题库
            question_bank.questions.add(question)
            question_bank.question_count = question_bank.questions.count()
            question_bank.save()

            return Response({
                "success": True,
                "message": f"Question {question_id} added to QuestionBank {question_bank_id} successfully."
            }, status=HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=HTTP_404_NOT_FOUND)

        except QuestionBank.DoesNotExist:
            return Response({"error": "QuestionBank not found."}, status=HTTP_404_NOT_FOUND)

        except Question.DoesNotExist:
            return Response({"error": "Question not found."}, status=HTTP_404_NOT_FOUND)

        except KeyError as e:
            return Response({"error": f"Missing required field: {str(e)}"}, status=HTTP_400_BAD_REQUEST)


class CreateQuestionInBank(APIView):
    def post(self, request):
        try:
            user_id = request.data['user_id']
            question_bank_id = request.data['question_bank_id']
            question_data = request.data['data']

            user = User.objects.get(id=user_id)
            question_bank = QuestionBank.objects.get(id=question_bank_id)

            if user.user_role != 1:  # 权限检查
                return Response({"error": "Only admins or teachers can create questions in a QuestionBank."},
                                status=HTTP_400_BAD_REQUEST)

            # 创建题目
            question = Question.objects.create(
                type=question_data['type'],
                content=question_data['content'],
                subject=question_data['subject'],
                added_at=question_data['added_at'],
                source=question_data.get('source'),
                tags=question_data.get('tags'),
                difficulty=question_data['difficulty'],
                answer=question_data.get('answer'),
                added_by=user,
                option_count=question_data.get('option_count', 0)
            )

            # 添加题目到题库
            question_bank.questions.add(question)
            question_bank.question_count = question_bank.questions.count()
            question_bank.save()

            return Response({
                "success": True,
                "message": f"Question created and added to QuestionBank {question_bank_id} successfully.",
                "question_id": question.id
            }, status=HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=HTTP_404_NOT_FOUND)

        except QuestionBank.DoesNotExist:
            return Response({"error": "QuestionBank not found."}, status=HTTP_404_NOT_FOUND)

        except KeyError as e:
            return Response({"error": f"Missing required field: {str(e)}"}, status=HTTP_400_BAD_REQUEST)


class RemoveQuestionFromBank(APIView):
    def post(self, request):
        try:
            user_id = request.data['user_id']
            question_bank_id = request.data['question_bank_id']
            question_id = request.data['question_id']

            user = User.objects.get(id=user_id)
            question_bank = QuestionBank.objects.get(id=question_bank_id)
            question = Question.objects.get(id=question_id)

            if user.user_role != 1:  # 权限检查
                return Response({"error": "Only admins or teachers can remove questions from a QuestionBank."},
                                status=HTTP_400_BAD_REQUEST)

            if question not in question_bank.questions.all():
                return Response({"error": "Question does not belong to this QuestionBank."},
                                status=HTTP_400_BAD_REQUEST)

            # 从题库移除题目
            question_bank.questions.remove(question)
            question_bank.question_count = question_bank.questions.count()
            question_bank.save()

            return Response({
                "success": True,
                "message": f"Question {question_id} removed from QuestionBank {question_bank_id} successfully."
            }, status=HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=HTTP_404_NOT_FOUND)

        except QuestionBank.DoesNotExist:
            return Response({"error": "QuestionBank not found."}, status=HTTP_404_NOT_FOUND)

        except Question.DoesNotExist:
            return Response({"error": "Question not found."}, status=HTTP_404_NOT_FOUND)

        except KeyError as e:
            return Response({"error": f"Missing required field: {str(e)}"}, status=HTTP_400_BAD_REQUEST)
