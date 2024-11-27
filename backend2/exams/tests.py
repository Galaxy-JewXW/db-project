from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from users.models import User
from questions.models import Question
from exams.models import Exam, ExamRecord
from utils.views import encode_password


class ExamTests(TestCase):
    def setUp(self):
        # 创建测试用户
        self.teacher = User.objects.create(
            id=1, student_id="T001", name="Teacher", password_digest=encode_password("123456"), user_role=1
        )
        self.student1 = User.objects.create(
            id=2, student_id="S001", name="Student1", password_digest=encode_password("123456"), user_role=2
        )
        self.student2 = User.objects.create(
            id=3, student_id="S002", name="Student2", password_digest=encode_password("123456"), user_role=2
        )

        # 创建多个题目
        self.question1 = Question.objects.create(
            type='单项选择题',
            content='What is the answer to life, the universe, and everything?',
            subject='基础物理学A',
            added_at='2024-11-20',
            difficulty='中等',
            tags=["Arithmetic"],
            answer='42',
            added_by=self.teacher
        )
        self.question2 = Question.objects.create(
            type='多项选择题',
            content='What is 2 + 2?',
            subject='工科高等代数',
            added_at='2024-11-21',
            difficulty='简单',
            tags=["Arithmetic"],
            answer='4',
            added_by=self.teacher
        )

        self.question3 = Question.objects.create(
            type='填空题',
            content='The capital of France is ____.',
            subject='离散数学（信息类）',
            added_at='2024-11-22',
            difficulty='简单',
            tags=["Geography"],
            answer='Paris',
            added_by=self.teacher
        )

        # 创建考试
        self.exam = Exam.objects.create(
            id=1,
            title="Math Exam",
            description="Test Math Exam",
            start_time="2024-12-01T09:00:00",
            end_time="2024-12-01T10:00:00",
            created_by=self.teacher,
        )
        self.exam.questions.add(self.question1, self.question2)
        self.exam.students.add(self.student1, self.student2)

        # 初始化 API 客户端
        self.client = APIClient()

    def test_create_exam(self):
        data = {
            "user_id": self.teacher.id,
            "title": "New Exam",
            "description": "This is a new exam",
            "start_time": "2024-12-01T08:00:00",
            "end_time": "2024-12-01T09:00:00",
            "questions": [self.question1.id],
        }
        response = self.client.post("/exams/create_exam", data, format="json")
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn("exam_id", response.data)
        self.assertEqual(Exam.objects.count(), 2)  # 新考试被创建

    def test_enroll_exam(self):
        data = {
            "user_id": self.student1.id,
            "exam_id": self.exam.id,
        }
        response = self.client.post("/exams/enroll_exam", data, format="json")
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn(self.student1, self.exam.students.all())

    def test_submit_answer(self):
        data = {
            "user_id": self.student1.id,
            "exam_id": self.exam.id,
            "question_id": self.question1.id,
            "submitted_answer": "4",
        }
        response = self.client.post("/exams/submit_answer", data, format="json")
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertTrue(ExamRecord.objects.filter(exam=self.exam, question=self.question1, student=self.student1).exists())

    def test_get_all_exams(self):
        response = self.client.post("/exams/get_all_exams", format="json")
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data["exams"]), 1)
        self.assertEqual(response.data["exams"][0]["title"], "Math Exam")

    def test_get_exam_questions(self):
        data = {
            "user_id": self.student1.id,
            "exam_id": self.exam.id,
        }
        response = self.client.post("/exams/get_exam_questions", data, format="json")
        print(response.data)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data["total_questions"], 2)
        self.assertEqual(len(response.data["questions"]), 5)  # 两种类型的题目

    def test_view_student_records_by_id(self):
        # 模拟提交作答
        ExamRecord.objects.create(
            exam=self.exam, question=self.question1, student=self.student1, submitted_answer="4", is_correct=True
        )
        data = {
            "user_id": self.teacher.id,
            "exam_id": self.exam.id,
            "student_id": self.student1.id,
        }
        response = self.client.post("/exams/view_student_records", data, format="json")
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data["records"]), 1)
        self.assertEqual(response.data["records"][0]["submitted_answer"], "4")

    def test_correct_answer(self):
        # 模拟提交作答
        record = ExamRecord.objects.create(
            exam=self.exam, question=self.question1, student=self.student1, submitted_answer="4", is_correct=False
        )
        data = {
            "user_id": self.teacher.id,
            "record_id": record.id,
            "is_correct": True,
        }
        response = self.client.post("/exams/correct_answer", data, format="json")
        self.assertEqual(response.status_code, HTTP_200_OK)
        record.refresh_from_db()
        self.assertTrue(record.is_correct)

    def test_get_exam_students(self):
        # 模拟学生作答
        ExamRecord.objects.create(
            exam=self.exam, question=self.question1, student=self.student1, submitted_answer="4", is_correct=True
        )
        data = {
            "user_id": self.teacher.id,
            "exam_id": self.exam.id,
        }
        response = self.client.post("/exams/get_exam_students", data, format="json")
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data["students"]), 2)
        self.assertEqual(response.data["students"][0]["exam_record"][0]["question_id"], self.question1.id)
