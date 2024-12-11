from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND

from broadcast.models import Broadcast
from message.models import Message
from questions.models import Question, UserQuestionRecord
from utils.views import decode_request
from django.http import JsonResponse
from users.models import User

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.permissions import AllowAny

@method_decorator(csrf_exempt, name='dispatch')
class GetHomeView(APIView):
    def post(self, request):
        try:
            user_id = request.data.get('user_id')  # 获取当前用户
            user = User.objects.get(student_id=user_id)
            # 获取最新公告（最多3条）
            broadcasts = Broadcast.objects.all().order_by('-sent_at')
            broadcast_data = [
                {
                    "id": b.id,
                    "sender": b.sender,
                    "sent_at": b.sent_at,
                    "last_updated": b.last_updated,
                    "title": b.title,
                    "content": b.content
                } for b in broadcasts
            ]

            # 获取最新未读消息（最多3条）
            messages = Message.objects.filter(receiver=user).order_by('-sent_at')
            message_data = [
                {
                    "id": m.id,
                    "sender": m.sender.name,
                    "sender_avatar": m.sender_avatar,
                    "sent_at": m.sent_at,
                    "content": m.content,
                    "is_read": m.is_read
                } for m in messages
            ]

            # 获取当前进度（各科目做题数量）
            progress_data = {}
            for subject, subject_display in Question.SUBJECT_CHOICES:
                user_question_count = UserQuestionRecord.objects.filter(user=user, question_subject=subject, is_correct=True).count()
                total_question_count = Question.objects.filter(subject=subject).count()
                progress_data[subject_display] = {
                    "subject": subject_display,
                    "user_question_count": user_question_count,
                    "total_question_count": total_question_count
                }

            # # 推荐题目
            # # 1. 获取最新错题（最多3道）
            wrong_questions = (
                UserQuestionRecord.objects.filter(user=user, is_correct=False)
                .order_by('-attempted_at')
                .values_list('question_id', flat=True)[:3]
            )
            wrong_questions_data = list(Question.objects.filter(id__in=wrong_questions))
            # 2. 获取剩余需要补足的题目
            num_wrong_questions = len(wrong_questions_data)
            num_additional_questions = max(0, 7 - num_wrong_questions)

            # 随机选取未做过的题目，排除错题
            remaining_questions = (
                Question.objects.exclude(id__in=wrong_questions)
                .exclude(user_records__user=user)
                .order_by('?')[:num_additional_questions]
            )

            # 合并错题和随机选题
            recommended_questions = wrong_questions_data + list(remaining_questions)
            recommended_questions_data = [
                {
                    "id": q.id,
                    "type": q.type,
                    "content": q.content,
                    "subject": q.subject,
                    "difficulty": q.difficulty,
                    "tags": q.tags
                } for q in recommended_questions
            ]
            recommended_exercise_data = [
                q.id
                for q in recommended_questions
            ]
            print(recommended_exercise_data)

            return Response({
                "success": True,
                "data": {
                    "notices": broadcast_data,
                    "messages": message_data,
                    "progress": progress_data,
                    # "recommended_questions": recommended_questions_data,
                    "recommendedExercises": recommended_exercise_data,
                }
            }, status=HTTP_200_OK)

        except User.DoesNotExist:
            return Response({
                'success': False,
                'error': 'User not found'
            }, status=HTTP_404_NOT_FOUND)

        except Question.DoesNotExist:
            return Response({"error": "Question not found."}, status=HTTP_404_NOT_FOUND)

        except Message.DoesNotExist:
            return Response({'error': 'Message not found'}, status=HTTP_404_NOT_FOUND)

        except Broadcast.DoesNotExist:
            return Response({'error': 'Broadcast not found'}, status=HTTP_404_NOT_FOUND)