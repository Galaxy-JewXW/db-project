from django.urls import path
from exams import views

urlpatterns = [
    # 创建考试
    path('create_exam', views.CreateExam.as_view(), name='create_exam'),

    # 学生报名考试
    path('enroll_exam', views.EnrollExam.as_view(), name='enroll_exam'),

    # 学生提交答案
    path('submit_answer', views.SubmitAnswer.as_view(), name='submit_answer'),

    # 老师查看学生的作答记录
    path('view_student_records', views.ViewStudentRecordsById.as_view(), name='view_student_records'),

    # 老师批改学生作答
    path('correct_answer', views.CorrectAnswer.as_view(), name='correct_answer'),

    # 获取所有考试
    path('get_all_exams', views.GetAllExams.as_view(), name='get_all_exams'),

    # 获取某一考试内所有题目
    path('get_exam_questions', views.GetExamQuestions.as_view(), name='get_exam_questions'),

    # 获取某一考试内所有参与学生的作答情况
    path('get_exam_students', views.GetExamStudents.as_view(), name='get_exam_students'),
]
