from django.urls import path
from questions import views

urlpatterns = [
    # 用户上传题目
    path('upload_question/', views.UploadQuestion.as_view(), name='upload_question'),

    # 用户完成题目
    path('complete_question/', views.CompleteQuestion.as_view(), name='complete_question'),

    # 创建题库
    path('create_questionbank/', views.CreateQuestionBank.as_view(), name='create_questionbank'),

    # 给题目写评论
    path('add_comment', views.AddComment.as_view(), name='add_comment'),

    # 点赞或取消点赞评论
    path('like_comment', views.LikeComment.as_view(), name='like_comment'),

    # 获取题目的所有评论
    path('get_question_comments', views.GetQuestionComments.as_view(), name='get_question_comments'),

    # 获取所有 QuestionBank
    path('get_all_question_banks/', views.GetAllQuestionBanks.as_view(), name='get_all_question_banks'),

    # 获取所有 Question
    path('get_all_questions/', views.GetAllQuestions.as_view(), name='get_all_questions'),

    # 获取某一科目的所有 Question
    path('get_questions_by_subject/', views.GetQuestionsBySubject.as_view(), name='get_questions_by_subject'),

    # 获取某一科目的所有 QuestionBank
    path('get_question_banks_by_subject/', views.GetQuestionBanksBySubject.as_view(), name='get_question_banks_by_subject'),

    # 获取某一 QuestionBank 内的所有 Question
    path('get_questions_by_questionbank/', views.GetQuestionsByQuestionBank.as_view(), name='get_questions_by_questionbank'),

    # 获取某一特定 id 的 Question 详细信息
    path('get_question_by_id/', views.GetQuestionById.as_view(), name='get_question_by_id'),

    # 删除某一特定 id 的题目
    path('delete_question/', views.DeleteQuestion.as_view(), name='delete_question'),

    path('get_questionbank/', views.GetQuestionBankById.as_view(), name='get_questionbank'),

    path('delete_questionbank/', views.DeleteQuestionBank.as_view(), name='delete_questionbank'),

    path('edit_question/', views.EditQuestion.as_view(), name='edit_question'),

    path('edit_question_in_bank', views.EditQuestionInBank.as_view(), name='edit_question_in_bank'),

    path('add_question_to_bank/', views.AddQuestionToBank.as_view(), name='add_question_to_bank'),

    path('create_question_in_bank', views.CreateQuestionInBank.as_view(), name='create_question_in_bank'),

    path('remove_question_from_bank/', views.RemoveQuestionFromBank.as_view(), name='remove_question_from_bank'),
    
    path('edit_questionbank/', views.EditQuestionBank.as_view(), name='edit_questionbank'),
]
