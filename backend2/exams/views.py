from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from utils.views import decode_request
from .models import Exam, Question, User, ExamRecord


class CreateExam(APIView):
    def post(self, request):
        try:
            data = decode_request(request)
            user_id = data.get('user_id')
            user = User.objects.get(id=user_id)

            if user.user_role != 1:  # 检查是否为老师
                return Response({"error": "Only teachers can create exams."}, status=HTTP_400_BAD_REQUEST)

            title = data.get('title')
            description = data.get('description')
            start_time = data.get('start_time')
            end_time = data.get('end_time')
            question_ids = data.get('questions')

            if not title or not start_time or not end_time:
                return Response({"error": "Missing required fields."}, status=HTTP_400_BAD_REQUEST)

            # 创建考试
            exam = Exam.objects.create(
                title=title,
                description=description,
                start_time=start_time,
                end_time=end_time,
                created_by=user
            )

            # 关联题目
            if question_ids:
                questions = Question.objects.filter(id__in=question_ids)
                exam.questions.add(*questions)

            return Response({"success": True, "exam_id": exam.id}, status=HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=HTTP_404_NOT_FOUND)


class EnrollExam(APIView):
    def post(self, request):
        try:
            data = decode_request(request)
            user_id = data.get('user_id')
            exam_id = data.get('exam_id')

            user = User.objects.get(id=user_id)
            exam = Exam.objects.get(id=exam_id)

            # 添加学生到考试
            exam.students.add(user)
            return Response({"success": True, "message": "Enrolled successfully."}, status=HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=HTTP_404_NOT_FOUND)
        except Exam.DoesNotExist:
            return Response({"error": "Exam not found."}, status=HTTP_404_NOT_FOUND)


class SubmitAnswer(APIView):
    def post(self, request):
        try:
            data = decode_request(request)
            user_id = data.get('user_id')
            exam_id = data.get('exam_id')
            question_id = data.get('question_id')
            submitted_answer = data.get('submitted_answer')

            user = User.objects.get(id=user_id)
            exam = Exam.objects.get(id=exam_id)
            question = Question.objects.get(id=question_id)

            # 确保学生已报名考试
            if user not in exam.students.all():
                return Response({"error": "You are not enrolled in this exam."}, status=HTTP_400_BAD_REQUEST)

            # 创建或更新做题记录（以最后一次为准）
            record, created = ExamRecord.objects.update_or_create(
                exam=exam, question=question, student=user,
                defaults={'submitted_answer': submitted_answer}
            )

            return Response({
                "success": True,
                "record_id": record.id,
                "answer_now": record.submitted_answer,
                "has_submitted": record.has_submitted()  # 确认学生是否提交了答案
            }, status=HTTP_200_OK)

        except (User.DoesNotExist, Exam.DoesNotExist, Question.DoesNotExist):
            return Response({"error": "Invalid exam, user, or question."}, status=HTTP_404_NOT_FOUND)


class GetExamQuestionById(APIView):
    def post(self, request):
        try:
            data = decode_request(request)
            user_id = data.get('user_id')
            exam_id = data.get('exam_id')
            question_id = data.get('question_id')

            user = User.objects.get(id=user_id)
            exam = Exam.objects.get(id=exam_id)
            question = Question.objects.get(id=question_id)

            # 确保学生已报名考试
            if user not in exam.students.all():
                return Response({"error": "You are not enrolled in this exam."}, status=HTTP_400_BAD_REQUEST)

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
            }

            try:
                exam_record = ExamRecord.objects.get(exam=exam, question=question, student=user)
                has_submitted = exam_record.has_submitted()
                answer_now = exam_record.submitted_answer
            except ExamRecord.DoesNotExist:
                answer_now = ""
                has_submitted = False

            return Response({
                "success": True,
                "question_data": question_data,
                "has_submitted": has_submitted,  # 确认学生是否提交了答案
                "answer_now": answer_now
            }, status=HTTP_200_OK)

        except (User.DoesNotExist, Exam.DoesNotExist, Question.DoesNotExist):
            return Response({"error": "Invalid exam, user, or question."}, status=HTTP_404_NOT_FOUND)


class ViewStudentRecordsById(APIView):
    def post(self, request):
        try:
            data = decode_request(request)
            user_id = data.get('user_id')
            exam_id = data.get('exam_id')
            student_id = data.get('student_id')

            user = User.objects.get(id=user_id)
            exam = Exam.objects.get(id=exam_id)
            student = User.objects.get(id=student_id)

            if user.user_role != 1:  # 检查是否为老师
                return Response({"error": "Only teachers can view records."}, status=HTTP_400_BAD_REQUEST)

            # 获取学生的所有记录
            records = ExamRecord.objects.filter(exam=exam, student=student)
            records_data = []
            for record in records:
                records_data.append({
                    "question_id": record.question.id,
                    "submitted_answer": record.submitted_answer,
                    "is_correct": record.is_correct
                })

            return Response({"success": True, "records": records_data}, status=HTTP_200_OK)

        except (User.DoesNotExist, Exam.DoesNotExist):
            return Response({"error": "Invalid user or exam."}, status=HTTP_404_NOT_FOUND)


class CorrectAnswer(APIView):
    def post(self, request):
        try:
            data = decode_request(request)
            user_id = data.get('user_id')
            record_id = data.get('record_id')
            is_correct = data.get('is_correct')

            user = User.objects.get(id=user_id)

            if user.user_role != 1:  # 检查是否为老师
                return Response({"error": "Only teachers can correct answers."}, status=HTTP_400_BAD_REQUEST)

            # 获取作答记录
            record = ExamRecord.objects.get(id=record_id)
            record.is_correct = is_correct
            record.save()

            return Response({"success": True, "message": "Answer corrected."}, status=HTTP_200_OK)

        except (User.DoesNotExist, ExamRecord.DoesNotExist):
            return Response({"error": "Invalid user or record."}, status=HTTP_404_NOT_FOUND)


class GetAllExams(APIView):
    """
    获取所有 Exam，按开始时间从远到近排序
    """

    def post(self, request):
        try:
            # 获取所有考试，按开始时间排序
            exams = Exam.objects.all().order_by('-start_time')

            # 构造返回数据
            exams_data = []
            for exam in exams:
                exams_data.append({
                    "id": exam.id,
                    "title": exam.title,
                    "description": exam.description,
                    "start_time": exam.start_time,
                    "end_time": exam.end_time,
                    "duration": exam.duration or exam.calculate_duration(),
                    "created_by": exam.created_by.name,
                    "student_count": exam.students.count(),
                    "question_count": exam.questions.count(),
                })

            return Response({
                "success": True,
                "exams": exams_data
            }, status=HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=HTTP_400_BAD_REQUEST)


class GetExamQuestions(APIView):
    """
    获取一个 Exam 内的所有题目，按题目类型分类并返回：
    - 题目 ID 列表
    - 每种类型的总题目数
    - 学生已提交该类型题目的数量
    - 整体题目总数和学生已提交题目总数
    """

    def post(self, request):
        try:
            # 解码请求数据
            data = decode_request(request)
            user_id = data.get("user_id")
            user = User.objects.get(id=user_id)
            exam_id = data.get("exam_id")
            exam = Exam.objects.get(id=exam_id)

            # 初始化返回数据
            questions_data = []
            total_questions = exam.questions.count()  # 总题目数
            total_submitted_questions = 0  # 已提交题目总数

            # 遍历题目类型并按类型获取题目数据
            for question_type, type_label in Question.TYPE_CHOICES:
                questions = exam.questions.filter(type=question_type).order_by("id")
                type_total = questions.count()  # 当前类型的总题目数
                type_submitted = 0  # 当前类型的已提交题目数

                # 获取当前类型题目数据
                type_questions = []
                for question in questions:
                    # 查询 ExamRecord 判断是否提交
                    try:
                        exam_record = ExamRecord.objects.get(exam=exam, question=question, student=user)
                        has_submitted = exam_record.has_submitted()
                    except ExamRecord.DoesNotExist:
                        has_submitted = False

                    # 统计已提交题目数量
                    if has_submitted:
                        type_submitted += 1

                    # 添加题目数据
                    type_questions.append({
                        "id": question.id,
                        "has_submitted": has_submitted
                    })

                # 累计总提交题目数
                total_submitted_questions += type_submitted

                # 按类型添加到结果
                questions_data.append({
                    "type": type_label,
                    "total": type_total,  # 当前类型的总题目数
                    "submitted": type_submitted,  # 当前类型的已提交题目数
                    "questions": type_questions  # 题目列表及提交状态
                })

            return Response({
                "success": True,
                "exam_id": exam.id,
                "total_questions": total_questions,  # 总题目数
                "total_submitted_questions": total_submitted_questions,  # 学生已提交题目数
                "questions": questions_data  # 按类型的题目数据
            }, status=HTTP_200_OK)

        except Exam.DoesNotExist:
            return Response({"error": "Exam not found."}, status=HTTP_404_NOT_FOUND)

        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=HTTP_404_NOT_FOUND)

        except KeyError as e:
            return Response({
                "success": False,
                "error": f"Missing required field: {str(e)}"
            }, status=HTTP_400_BAD_REQUEST)


class GetExamStudents(APIView):
    """
    获取某一考试内所有参与学生的作答情况，按学号从小到大排序。
    """

    def post(self, request):
        try:
            data = decode_request(request)
            user_id = data.get("user_id")
            user = User.objects.get(id=user_id)
            exam_id = data.get("exam_id")
            exam = Exam.objects.get(id=exam_id)

            # 确保请求的用户是老师 (user_role == 1)
            if user.user_role != 1:
                return Response({
                    "success": False,
                    "error": "权限不足",
                    "message": "权限不足"
                }, status=HTTP_400_BAD_REQUEST)

            # 获取所有参与该考试的学生（通过Exam.students）
            students = exam.students.all().order_by("student_id")

            # 获取学生的作答记录
            students_data = []
            for student in students:
                student_data = {
                    "student_id": student.student_id,
                    "name": student.name,
                    "exam_record": []
                }

                # 获取该学生的所有做题记录，按题目id排序
                exam_records = ExamRecord.objects.filter(exam=exam, student=student).order_by("question__id")
                if exam_records.exists():
                    for record in exam_records:
                        student_data["exam_record"].append({
                            "question_id": record.question.id,
                            "submitted_answer": record.submitted_answer,
                            "is_correct": record.is_correct,
                            "submitted_at": record.submitted_at
                        })
                else:
                    # 如果没有做题记录，可以返回一个空的 `exam_record` 或者一个适当的默认值
                    student_data["exam_record"] = None

                students_data.append(student_data)

            return Response({
                "success": True,
                "exam_id": exam.id,
                "students": students_data
            }, status=HTTP_200_OK)

        except Exam.DoesNotExist:
            return Response({"error": "Exam not found."}, status=HTTP_404_NOT_FOUND)

        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=HTTP_404_NOT_FOUND)

        except KeyError as e:
            return Response({
                "success": False,
                "error": f"Missing required field: {str(e)}"
            }, status=HTTP_400_BAD_REQUEST)
