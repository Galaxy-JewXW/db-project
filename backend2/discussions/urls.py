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
    GetDiscussionById,
    LikeReply,
    DeleteDiscussion,
    DeleteReply,
    MarkDiscussion
)

urlpatterns = [
    path('delete_discussion/', DeleteDiscussion.as_view(), name='delete_discussion'),
    path('delete_reply/', DeleteReply.as_view(), name='delete_reply'),
    path('create_discussion/', CreateDiscussion.as_view(), name='create_discussion'), #ok
    path('like_discussion/', LikePost.as_view(), name='like_discussion'), #ok
    path('like_reply/', LikeReply.as_view(), name='like_reply'), #ok
    path('subscribe_discussion/', SubscribeDiscussion.as_view(), name='subscribe_discussion'), #ok
    path('create_reply/', CreateReply.as_view(), name='create_reply'), #ok
    path('edit_discussion/', EditDiscussion.as_view(), name='edit_discussion'), #ok
    path('edit_reply/', EditReply.as_view(), name='edit_reply'), #ok
    path('get_all_discussions/', GetAllDiscussions.as_view(), name='get_all_discussions'), #ok
    path('get_discussion_replies/', GetDiscussionReplies.as_view(), name='get_discussion_replies'),
    path('get_discussion/', GetDiscussionById.as_view(), name='get_discussion'), #ok
    path('mark_discussion/', MarkDiscussion.as_view(), name='mark_discussion'), #ok
]
