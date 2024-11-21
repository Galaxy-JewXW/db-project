from django.urls import path
from learingCompanionInBeihang.apps.questions import views

urlpatterns = [
    # 用户上传题目
    path('upload_question', views.UploadQuestion.as_view(), name='upload_question'),

    # 用户完成题目
    path('complete_question', views.CompleteQuestion.as_view(), name='complete_question'),

    # 创建题库
    path('create_questionbank', views.CreateQuestionBank.as_view(), name='create_questionbank'),

    # 给题目写评论
    path('add_comment', views.AddComment.as_view(), name='add_comment'),

    # 点赞或取消点赞评论
    path('like_comment', views.LikeComment.as_view(), name='like_comment'),

    # 获取题目的所有评论
    path('get_question_comments', views.GetQuestionComments.as_view(), name='get_question_comments'),
]
