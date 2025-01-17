from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from utils.views import decode_request
from questions.models import QuestionBank
from .models import Exam, Question, User, ExamRecord


class CreateExam(APIView):
    def post(self, request):
        try:
            data = decode_request(request)
            user_id = data.get('user_id')
            user = User.objects.get(student_id=user_id)

            if user.user_role != 1:  # 检查是否为老师
                return Response({"error": "Only teachers can create exams."}, status=HTTP_400_BAD_REQUEST)

            title = data.get('title')
            subject = data.get('subject')
            start_time = data.get('start_time')
            duration = data.get('duration')
            question_ids = data.get('questions')
            print(question_ids)
            all_ids = []
            for que in question_ids:
                for item in que['questions']:
                    all_ids.append(item['id'])
            if not title or not start_time or not duration:
                return Response({"error": "Missing required fields."}, status=HTTP_400_BAD_REQUEST)

            # 创建考试
            exam = Exam.objects.create(
                title=title,
                subject=subject,
                start_time=start_time,
                duration=duration,
                created_by=user
            )

            # 关联题目
            all_questions = Question.objects.all()

            # 手动筛选 id 在 all_ids 中的问题
            filtered_questions = []
            for question in all_questions:
                if question.id in all_ids:
                    filtered_questions.append(question)

            # 转换为列表以保持与 QuerySet 的一致性
            questions = list(filtered_questions)
            exam.questions.add(*questions)

            return Response({"success": True, "exam_id": exam.id}, status=HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=HTTP_404_NOT_FOUND)


class EnrollExam(APIView):
    def post(self, request):
        try:
            print("to here")
            data = decode_request(request)
            user_id = data.get('user_id')
            exam_id = data.get('exam_id')

            user = User.objects.get(student_id=user_id)
            exam = Exam.objects.get(id=exam_id)
            print(user_id)
            print(user)
            print(exam)

            # 添加学生到考试 或 取消报名
            if user in exam.students.all():
                exam.students.remove(user)
            else:
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
            print(submitted_answer)
            user = User.objects.get(student_id=user_id)
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

            if question.is_true_false() or question.is_single_choice() or question.is_multiple_choice():
                if submitted_answer == question.answer:
                    record.is_correct = True
                else:
                    record.is_correct = False
                record.is_checked = True
                record.save()

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

            user = User.objects.get(student_id=user_id)
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

            # 获取学生的所有记录
            records = ExamRecord.objects.filter(exam=exam, student=student)
            records_data = []
            for record in records:
                records_data.append({
                    "question_id": record.question.id,
                    "question_answer": record.question.answer,
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
            student_id = data.get('student_id')
            user_id = data.get('user_id')
            exam_id = data.get('exam_id')
            question_id = data.get('question_id')
            print(student_id)
            print(exam_id)
            print(user_id)
            print(question_id)
            is_correct = data.get('is_correct')
            print(is_correct)
            user = User.objects.get(student_id=user_id)
            question = Question.objects.get(id=question_id)
            exam = Exam.objects.get(id=exam_id)
            student = User.objects.get(student_id=student_id)
            print(student)
            print(exam)
            print(question)
            if user.user_role != 1:  # 检查是否为老师
                return Response({"error": "Only teachers can correct answers."}, status=HTTP_400_BAD_REQUEST)

            # 获取作答记录
            record = ExamRecord.objects.get(student=student, exam=exam, question=question)
            print(record)
            record.is_correct = is_correct
            record.is_checked = True
            record.save()

            return Response({"success": True, "message": "Answer corrected."}, status=HTTP_200_OK)

        except (User.DoesNotExist):
            return Response({"error": "Invalid user or record."}, status=HTTP_404_NOT_FOUND)

        except (ExamRecord.DoesNotExist):
            return Response({"success": True, "message": "Answer corrected."}, status=HTTP_200_OK)


class GetAllExams(APIView):
    """
    获取所有 Exam，按开始时间从远到近排序
    """

    def post(self, request):
        try:
            # 获取所有考试，按开始时间排序 
            data = decode_request(request)
            user = None
            if data.get('user_id'):
                user_id = data.get('user_id')
                user = User.objects.get(student_id=user_id)

            exams = Exam.objects.all().order_by('-start_time')
            # 构造返回数据
            exams_data = []
            ongoing_exams = []
            coming_exams = []
            past_exams = []
            enrolled_exams = []
            print(user)
            for exam in exams:
                if exam.get_status() == "coming":
                    coming_exams.append({
                        "id": exam.id,
                        "name": exam.title,
                        "description": exam.description,
                        "starttime": exam.start_time,
                        "subject": exam.subject,
                        "duration": exam.duration,
                        "createdAt": exam.created_at,
                        "created_by": exam.created_by.name,
                        "is_checked": exam.is_checked,
                        "is_published": exam.is_published,
                        "student_count": exam.students.count(),
                        "question_count": exam.questions.count(),
                    })
                elif exam.get_status() == "past" and ((exam.is_published and user in exam.students.all()) or (user!=None and user.user_role>=1)):
                    past_exams.append({
                        "id": exam.id,
                        "name": exam.title,
                        "description": exam.description,
                        "starttime": exam.start_time,
                        "subject": exam.subject,
                        "duration": exam.duration,
                        "createdAt": exam.created_at,
                        "created_by": exam.created_by.name,
                        "is_checked": exam.is_checked,
                        "is_published": exam.is_published,
                        "student_count": exam.students.count(),
                        "question_count": exam.questions.count(),
                    })
                elif exam.get_status() == "ongoing":
                    ongoing_exams.append({
                        "id": exam.id,
                        "name": exam.title,
                        "description": exam.description,
                        "starttime": exam.start_time,
                        "subject": exam.subject,
                        "duration": exam.duration,
                        "createdAt": exam.created_at,
                        "created_by": exam.created_by.name,
                        "is_checked": exam.is_checked,
                        "is_published": exam.is_published,
                        "student_count": exam.students.count(),
                        "question_count": exam.questions.count(),
                    })
                if user in exam.students.all():
                    enrolled_exams.append(exam.id)
                exams_data.append({
                    "id": exam.id,
                    "name": exam.title,
                    "description": exam.description,
                    "starttime": exam.start_time,
                    "subject": exam.subject,
                    "duration": exam.duration,
                    "createdAt": exam.created_at,
                    "created_by": exam.created_by.name,
                    "ready": exam.is_checked,
                    "disclosed": exam.is_published,
                    "student_count": exam.students.count(),
                    "question_count": exam.questions.count(),
                })
            print(exams_data)
            return Response({
                "success": True,
                "exams": exams_data,
                "ongoing_exams": ongoing_exams,
                "past_exams": past_exams,
                "enrolled_exams": enrolled_exams,
                "coming_exams": coming_exams,
            }, status=HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=HTTP_400_BAD_REQUEST)


class GetExamQuestionsTeacher(APIView):
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
            print("to here")
            data = decode_request(request)
            user_id = data.get("user_id")
            user = User.objects.get(student_id=user_id)
            exam_id = data.get("exam_id")
            exam = Exam.objects.get(id=exam_id)

            # 初始化返回数据
            questions_data = []
            total_questions = exam.questions.count()  # 总题目数
            total_checked_questions = 0  # 已提交题目总数

            students = exam.students.all()
            uid = []
            new_que = []
            # 遍历题目类型并按类型获取题目数据
            for question_type, type_label in Question.TYPE_CHOICES:
                questions = exam.questions.filter(type=question_type).order_by("id")
                type_total = questions.count()  # 当前类型的总题目数
                type_checked = 0  # 当前类型的已提交题目数
                # 获取当前类型题目数据
                type_questions = []
                fid = []
                for question in questions:
                    # 查询 ExamRecord 判断是否提交
                    has_checked = True
                    for student in students:
                        try:
                            exam_record = ExamRecord.objects.get(exam=exam, question=question, student=student)
                            has_checked = exam_record.is_checked
                            if not has_checked:
                                break
                        except ExamRecord.DoesNotExist:
                            has_checked = True

                    # 统计已提交题目数量
                    if has_checked:
                        total_checked_questions = total_checked_questions + 1
                        uid.append(question.id)
                    fid.append(question.id)
                    # 添加题目数据
                    type_questions.append({
                        "id": question.id,
                        "has_checked": has_checked,
                        "score": 100,
                    })

                new_que.append({
                    "type": type_label,
                    "currentPage": 1,
                    "ids": fid,
                })
                questions_data.append({
                    "currentPage": 1,
                    "type": type_label,
                    "questions": type_questions,
                })
                # 累计总提交题目数
                # total_checked_questions += type_checked

                # 按类型添加到结果
                # questions_data.append({
                #     "type": type_label,
                #     "total": type_total,  # 当前类型的总题目数
                #     "checked": type_checked,  # 当前类型的已提交题目数
                #     "questions": type_questions  # 题目列表及提交状态
                # })
            print(exam.is_checked)
            print(total_checked_questions)
            print(total_questions)
            if total_checked_questions == total_questions:
                exam.is_checked = True
            else:
                exam.is_checked = False

            exam.save()
            print(exam.start_time)
            print(exam.is_checked)
            print(exam)
            return Response({
                "success": True,
                "name": exam.title,
                "subject": exam.subject,
                "startTime": exam.start_time,
                "duration": exam.duration,
                "exam_id": exam.id,
                "finish": uid,
                "is_checked": exam.is_checked,
                "is_published": exam.is_published,
                "total_questions": total_questions,  # 总题目数
                "total_checked_questions": total_checked_questions,  # 学生已提交题目数
                "questions": questions_data,  # 按类型的题目数据
                "new_que": new_que,
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
            user = User.objects.get(student_id=user_id)
            exam_id = data.get("exam_id")
            exam = Exam.objects.get(id=exam_id)

            # 初始化返回数据
            questions_data = []
            total_questions = exam.questions.count()  # 总题目数
            total_submitted_questions = 0  # 已提交题目总数
            fid = []
            # 遍历题目类型并按类型获取题目数据
            for question_type, type_label in Question.TYPE_CHOICES:
                questions = exam.questions.filter(type=question_type).order_by("id")
                type_total = questions.count()  # 当前类型的总题目数
                type_submitted = 0  # 当前类型的已提交题目数

                # 获取当前类型题目数据
                type_questions = []
                uid = []
                for question in questions:
                    # 查询 ExamRecord 判断是否提交
                    try:
                        exam_record = ExamRecord.objects.get(exam=exam, question=question, student=user)
                        has_submitted = exam_record.has_submitted()
                    except ExamRecord.DoesNotExist:
                        has_submitted = False

                    # 统计已提交题目数量
                    if has_submitted:
                        fid.append(question.id)

                    uid.append(question.id)
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
                    "ids": uid,
                    "currentPage": 1
                })

            return Response({
                "success": True,
                "id": exam.id,
                "name": exam.title,
                "subject": exam.subject,
                "starttime": exam.start_time,
                "duration": exam.duration,
                "total_questions": total_questions,  # 总题目数
                "total_submitted_questions": total_submitted_questions,  # 学生已提交题目数
                "questions": questions_data,  # 按类型的题目数据
                "qsdata": questions_data,
                "finish": fid
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


class GetExamQuestionOfStudents(APIView):
    """
    获取某一考试内指定题目所有学生的作答情况。
    """

    def post(self, request):
        try:
            data = decode_request(request)
            user_id = data.get("user_id")
            question_id = data.get("question_id")
            exam_id = data.get("exam_id")

            # 验证用户和权限
            user = User.objects.get(student_id=user_id)
            if user.user_role != 1:  # 检查用户是否为老师
                return Response({
                    "success": False,
                    "error": "权限不足",
                    "message": "只有老师可以查看学生作答情况。"
                }, status=HTTP_400_BAD_REQUEST)

            # 获取考试和题目
            exam = Exam.objects.get(id=exam_id)
            question = exam.questions.get(id=question_id)  # 确保题目属于该考试

            # 获取参与该考试的所有学生
            students = exam.students.all().order_by("student_id")

            # 获取学生作答情况
            students_data = []
            for student in students:
                try:
                    # 查找学生的作答记录
                    record = ExamRecord.objects.get(exam=exam, question=question, student=student)
                    students_data.append({
                        "student": student.student_id,
                        "name": student.name,
                        "answer": record.submitted_answer,
                        "isCorrect": record.is_correct,
                        "submitted_at": record.submitted_at
                    })
                except ExamRecord.DoesNotExist:
                    pass

            return Response({
                "type": question.type,
                "success": True,
                "exam_id": exam.id,
                "question_id": question.id,
                "question_answer": question.answer,
                "students": students_data
            }, status=HTTP_200_OK)

        except Exam.DoesNotExist:
            return Response({"error": "Exam not found."}, status=HTTP_404_NOT_FOUND)

        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=HTTP_404_NOT_FOUND)

        except Question.DoesNotExist:
            return Response({"error": "Question not found in the specified exam."}, status=HTTP_404_NOT_FOUND)

        except KeyError as e:
            return Response({
                "success": False,
                "error": f"Missing required field: {str(e)}"
            }, status=HTTP_400_BAD_REQUEST)


class EditExam(APIView):
    def post(self, request):
        try:
            data = decode_request(request)
            user_id = data.get('user_id')
            user = User.objects.get(student_id=user_id)
            exam_id = data.get('exam_id')
            print(user_id)
            print(exam_id)
            exam = Exam.objects.get(id=exam_id)

            if user.user_role != 1 and exam.creator != user:  # 检查是否为老师
                return Response({"error": "Only teachers can create exams."}, status=HTTP_400_BAD_REQUEST)

            title = data.get('title')
            subject = data.get('subject')
            start_time = data.get('start_time')
            duration = data.get('duration')
            questions = data.get('questions')
            print(questions)
            all_ids = []
            for que in questions:
                for item in que['questions']:
                    all_ids.append(item['id'])
            print(title)

            exam.title = title
            exam.subject = subject
            exam.start_time = start_time
            exam.duration = duration

            all_questions = Question.objects.all()

            # 手动筛选 id 在 all_ids 中的问题
            filtered_questions = []
            for question in all_questions:
                if question.id in all_ids:
                    filtered_questions.append(question)

            # 转换为列表以保持与 QuerySet 的一致性
            new_questions = list(filtered_questions)
            # 关联题目
            # new_questions = Question.objects.filter(id__in=all_ids)
            exam.questions.set(new_questions)

            exam.save()

            return Response({"success": True, "exam_id": exam.id}, status=HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=HTTP_404_NOT_FOUND)

        except Exam.DoesNotExist:
            return Response({"error": "Exam not found"}, status=HTTP_404_NOT_FOUND)
        except Question.DoesNotExist:
            return Response({"error": "Question not found"}, status=HTTP_404_NOT_FOUND)


class ViewExamQuestionsResults(APIView):
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
            user = User.objects.get(student_id=user_id)
            exam_id = data.get("exam_id")
            exam = Exam.objects.get(id=exam_id)

            # 初始化返回数据
            questions_data = []
            total_questions = exam.questions.count()  # 总题目数
            total_correct_questions = 0  # 已提交题目总数
            uid = []
            # 遍历题目类型并按类型获取题目数据
            for question_type, type_label in Question.TYPE_CHOICES:
                questions = exam.questions.filter(type=question_type).order_by("id")
                type_total = questions.count()  # 当前类型的总题目数
                type_correct = 0  # 当前类型的已提交题目数

                # 获取当前类型题目数据
                type_questions = []
                for question in questions:
                    # 查询 ExamRecord 判断是否提交
                    try:
                        exam_record = ExamRecord.objects.get(exam=exam, question=question, student=user)
                        has_submitted = exam_record.has_submitted()
                        answer_now = exam_record.submitted_answer
                        is_correct = exam_record.is_correct
                    except ExamRecord.DoesNotExist:
                        answer_now = ""
                        is_correct = False

                    # 统计已提交题目数量
                    if is_correct:
                        uid.append(question.id)
                        type_correct += 1

                    # 添加题目数据
                    type_questions.append({
                        "id": question.id,
                        "correct": is_correct,
                    })

                # 累计总提交题目数
                total_correct_questions += type_correct

                # 按类型添加到结果
                questions_data.append({
                    "type": type_label,
                    "total": type_total,  # 当前类型的总题目数
                    "correct": type_correct,  # 当前类型的已提交题目数
                    "questions": type_questions  # 题目列表及提交状态
                })

            return Response({
                "success": True,
                "name": exam.title,
                "subject": exam.subject,
                "starttime": exam.start_time,
                "duration": exam.duration,
                "exam_id": exam.id,
                "total_questions": total_questions,  # 总题目数
                "total_correct_questions": total_correct_questions,  # 学生已提交题目数
                "questions": questions_data,  # 按类型的题目数据
                "finished": uid,
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


class ViewQuestionResult(APIView):
    def post(self, request):
        try:
            data = decode_request(request)
            user_id = data.get('user_id')
            exam_id = data.get('exam_id')
            question_id = data.get('question_id')

            user = User.objects.get(student_id=user_id)
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
                is_correct = exam_record.is_correct
            except ExamRecord.DoesNotExist:
                answer_now = ""
                is_correct = False

            return Response({
                "success": True,
                "question_data": question_data,
                "is_correct": is_correct,  # 确认学生是否提交了答案
                "answer_now": answer_now
            }, status=HTTP_200_OK)

        except (User.DoesNotExist, Exam.DoesNotExist, Question.DoesNotExist):
            return Response({"error": "Invalid exam, user, or question."}, status=HTTP_404_NOT_FOUND)


class DeleteExam(APIView):
    """
    删除指定考试的视图函数。
    只有管理员或考试的创建者可以删除考试。
    """

    def post(self, request):
        try:
            # 获取请求数据
            data = decode_request(request)
            user_id = data.get("user_id")  # 当前请求用户
            exam_id = data.get("exam_id")  # 要删除的考试ID
            print(user_id)
            print(exam_id)
            # 验证用户身份
            user = User.objects.get(student_id=user_id)
            exam = Exam.objects.get(id=exam_id)
            print(user)
            print(exam)
            # 检查权限：管理员或考试创建者
            if user.user_role < 1 and exam.created_by != user:
                return Response({
                    "success": False,
                    "error": "权限不足",
                    "message": "只有管理员或考试创建者可以删除考试。"
                }, status=HTTP_400_BAD_REQUEST)

            # 删除考试
            exam.delete()
            return Response({
                "success": True,
                "message": f"考试 {exam_id} 已成功删除。"
            }, status=HTTP_200_OK)

        except User.DoesNotExist:
            return Response({
                "success": False,
                "error": "用户未找到。"
            }, status=HTTP_404_NOT_FOUND)

        except Exam.DoesNotExist:
            return Response({
                "success": False,
                "error": "考试未找到。"
            }, status=HTTP_404_NOT_FOUND)

        except KeyError as e:
            return Response({
                "success": False,
                "error": f"缺少必要字段: {str(e)}"
            }, status=HTTP_400_BAD_REQUEST)


class PublishExamResults(APIView):
    """
    老师公开考试结果的视图函数。
    只有老师可以将考试结果设为公开。
    """

    def post(self, request):
        try:
            data = decode_request(request)
            user_id = data.get("user_id")
            exam_id = data.get("exam_id")

            # 获取用户和考试信息
            user = User.objects.get(student_id=user_id)
            exam = Exam.objects.get(id=exam_id)

            # 检查权限：只有老师可以公开考试结果
            if user.user_role != 1:
                return Response({
                    "success": False,
                    "error": "权限不足",
                    "message": "只有老师可以公开考试结果。"
                }, status=HTTP_400_BAD_REQUEST)

            # 更新考试的公开状态
            exam.is_published = not exam.is_published
            exam.save()

            question_bank = QuestionBank.objects.create(
                subject = exam.subject,
                estimated_time = exam.duration,
                creator = user,
                description = f"这是{exam.title}的题目",
                name = exam.title
            )

            questions = exam.questions.all()
            question_bank.questions.set(questions)
            question_bank.question_count = questions.count()
            question_bank.save()

            return Response({
                "success": True,
                "message": f"考试 {exam_id} 的结果已公开。"
            }, status=HTTP_200_OK)

        except User.DoesNotExist:
            return Response({
                "success": False,
                "error": "用户未找到。"
            }, status=HTTP_404_NOT_FOUND)

        except Exam.DoesNotExist:
            return Response({
                "success": False,
                "error": "考试未找到。"
            }, status=HTTP_404_NOT_FOUND)

        except KeyError as e:
            return Response({
                "success": False,
                "error": f"缺少必要字段: {str(e)}"
            }, status=HTTP_400_BAD_REQUEST)


class GetExamPublishStatus(APIView):
    """
    获取当前考试的公开状态。
    """

    def post(self, request):
        try:
            data = decode_request(request)
            exam_id = data.get("exam_id")

            # 获取考试信息
            exam = Exam.objects.get(id=exam_id)

            return Response({
                "success": True,
                "exam_id": exam.id,
                "is_published": exam.is_published
            }, status=HTTP_200_OK)

        except Exam.DoesNotExist:
            return Response({
                "success": False,
                "error": "考试未找到。"
            }, status=HTTP_404_NOT_FOUND)

        except KeyError as e:
            return Response({
                "success": False,
                "error": f"缺少必要字段: {str(e)}"
            }, status=HTTP_400_BAD_REQUEST)
