from django.urls import path
from .views import (
    CreateDiscussion,
    LikePost,
    SubscribeDiscussion,
    CreateReply,
    EditDiscussion,
    EditReply,
    GetAllDiscussions,
    GetDiscussionReplies,
    GetDiscussionById
)

urlpatterns = [
    path('create_discussion/', CreateDiscussion.as_view(), name='create_discussion'),
    path('like_discussion', LikePost.as_view(), name='like_discussion'),
    path('subscribe_discussion', SubscribeDiscussion.as_view(), name='subscribe_discussion'),
    path('create_reply', CreateReply.as_view(), name='create_reply'),
    path('edit_discussion', EditDiscussion.as_view(), name='edit_discussion'),
    path('edit_reply', EditReply.as_view(), name='edit_reply'),
    path('get_all_discussions', GetAllDiscussions.as_view(), name='get_all_discussions'),
    path('get_discussion_replies', GetDiscussionReplies.as_view(), name='get_discussion_replies'),
    path('get_discussion', GetDiscussionById.as_view(), name='get_discussion'),
]
