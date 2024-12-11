from django.urls import path
from broadcast import views

urlpatterns = [
    # 发布新的广播
    path('publish_broadcast', views.PublishBroadcast.as_view(), name='publish_broadcast'),

    # 编辑现有广播
    path('edit_broadcast', views.EditBroadcast.as_view(), name='edit_broadcast'),

    # 删除广播
    path('delete_broadcast', views.DeleteBroadcast.as_view(), name='delete_broadcast'),

    # 获取所有广播消息（仅管理员权限）
    path('get_all_broadcasts', views.GetAllBroadcasts.as_view(), name='get_all_broadcasts'),

    # 获取指定 ID 的广播消息（仅管理员权限）
    path('get_broadcast_by_id', views.GetBroadcastById.as_view(), name='get_broadcast_by_id'),
]
