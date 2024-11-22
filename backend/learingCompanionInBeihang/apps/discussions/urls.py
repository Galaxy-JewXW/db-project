from django.urls import path
from learingCompanionInBeihang.apps.discussions import views

urlpatterns = [
    # Create a new discussion
    path('create_discussion', views.CreateDiscussion.as_view(), name='create_discussion'),

    # Like or unlike a discussion
    path('like_discussion', views.LikePost.as_view(), name='like_discussion'),

    # Subscribe or unsubscribe to a discussion
    path('subscribe_discussion', views.SubscribeDiscussion.as_view(), name='subscribe_discussion'),

    # Create a reply to a discussion
    path('create_reply', views.CreateReply.as_view(), name='create_reply'),

    # Edit a discussion
    path('edit_discussion', views.EditDiscussion.as_view(), name='edit_discussion'),

    # Edit a reply
    path('edit_reply', views.EditReply.as_view(), name='edit_reply'),

    # Get all discussions with filters
    path('get_all_discussions', views.GetAllDiscussions.as_view(), name='get_all_discussions'),

    # Get replies for a specific discussion
    path('get_discussion_replies', views.GetDiscussionReplies.as_view(), name='get_discussion_replies'),

    # Get detailed information for a specific discussion, including replies
    path('get_discussion', views.GetDiscussionById.as_view(), name='get_discussion'),
]
