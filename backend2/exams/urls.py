from django.urls import path
from exams import views

urlpatterns = [
    # 创建考试
    path('create_exam', views.CreateExam.as_view(), name='create_exam'),

    # 学生报名考试|取消报名
    path('enroll_exam', views.EnrollExam.as_view(), name='enroll_exam'),

    # 学生提交答案
    path('submit_answer', views.SubmitAnswer.as_view(), name='submit_answer'),

    # 老师查看学生的作答记录|学生获取自己的所有批改情况
    path('view_student_records', views.ViewStudentRecordsById.as_view(), name='view_student_records'),

    # 老师批改学生作答
    path('correct_answer', views.CorrectAnswer.as_view(), name='correct_answer'),

    # 获取所有考试
    path('get_all_exams', views.GetAllExams.as_view(), name='get_all_exams'),

    # 获取某一考试内所有题目|包含学生是否已经作答，作答几题
    path('get_exam_questions', views.GetExamQuestions.as_view(), name='get_exam_questions'),

    # 获取某一考试内所有参与学生的作答情况
    path('get_exam_students', views.GetExamStudents.as_view(), name='get_exam_students'),
    # 获取考试内当前学生查看某题的信息，包含题目信息和学生的已有作答
    path('get_exam_student_questions', views.GetExamQuestionById.as_view(), name='get_exam_student_questions'),
    # 编辑考试
    path('edit_exam', views.EditExam.as_view(), name='edit_exam'),
    # 删除考试
    path('delete_exam', views.DeleteExam.as_view(), name='delete_exam'),
    # 获取某道题目所有学生的作答情况
    path('get_exam_questions_students', views.GetExamQuestionOfStudents.as_view(), name='get_exam_questions_students'),
    # 学生查看某一题目批改情况
    path('view_question_result', views.ViewQuestionResult.as_view(), name='view_question_result'),
    # 老师更改考试结果公开状态
    path('publish_exam_results', views.PublishExamResults.as_view(), name='publish_exam_results'),
    # 学生获取考试信息是否公开
    path('get_exam_publish_status', views.GetExamPublishStatus.as_view(), name='get_exam_publish_status'),
    # 老师获取当前考试批改状态
    path('get_exam_questions_teacher', views.GetExamQuestionsTeacher.as_view(), name='get_exam_questions_teacher'),
]
