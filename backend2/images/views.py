from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from backend2.settings import MEDIA_ROOT, STATIC_URL
from users.models import User
from utils.views import check_role, response_json
from utils.constants import ImageErrorCode, UserRole

import os
import uuid
import imghdr
from datetime import datetime

# Create your views here.

PIC_URL_BASE = 'http://localhost:8000'


class UploadAvatar(APIView):

    def post(self, request, action_user=None):
        pass


class UploadImage(APIView):

    @check_role(UserRole.ALL_USERS)
    def post(self, request, action_user: User = None):
        try:
            image = request.data['file']
            image_type = imghdr.what(image)
            # print(type(image))
        except Exception as _e:
            # raise _e
            return Response(response_json(
                success=False,
                code=ImageErrorCode.IMAGE_LOAD_FAILED,
                message="image load failed!"
            ))
        if image.size > (5 << 20):  # 5MB
            return Response(response_json(
                success=False,
                code=ImageErrorCode.IMAGE_TOO_BIG,
                message="size of uploaded image can't exceed 5MB!"
            ))
        if image_type is None:
            return Response(response_json(
                success=False,
                code=ImageErrorCode.INVALID_IMAGE_FORMAT,
                message="not an image-format file!"
            ))

        image_root = os.path.join(MEDIA_ROOT)
        # image_name = action_user.student_id + '_' + datetime.now().strftime("%Y%m%d%H%M%S") + '_' + str(uuid.uuid4()) + '.' + image_type
        image_name = datetime.now().strftime("%Y%m%d%H%M%S") + '_' + str(uuid.uuid4()) + '.' + image_type
        image_path = os.path.join(image_root, image_name)
        # get file
        img_suffix = image.name.split('.')[-1]
        if image_type != ('jpeg' if img_suffix == 'jpg' else img_suffix):
            return Response(response_json(
                success=False,
                code=ImageErrorCode.UNEXPECTED_IMAGE_NAME,
                message='wrong image suffix!'
            ))
        # store file
        try:
            print(image_root)
            if not os.path.exists(image_root):
                os.mkdir(image_root)
            with open(image_path, 'wb+') as f:
                for chunk in image.chunks():
                    f.write(chunk)
                f.close()
            print(PIC_URL_BASE + STATIC_URL)
        except Exception as _e:
            return Response(response_json(
                success=False,
                code=ImageErrorCode.IMAGE_SAVE_FAILED,
                message='image save failed!'
            ))
        return Response(response_json(
            success=True,
            message='upload image successfully!',
            data={
                'url': PIC_URL_BASE + image_name
            }
        ))

import os
from datetime import datetime
from django.conf import settings
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.utils.http import urlsafe_base64_encode
from .upload_images import upload  # 导入上传到腾讯云的 upload 方法
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.permissions import AllowAny

@method_decorator(csrf_exempt, name='dispatch')
# 允许上传的文件类型
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 上传头像的视图

@method_decorator(csrf_exempt, name='dispatch')
def upload_avatar(request):
    if request.method == 'POST' and request.FILES.get('avatar'):
        avatar = request.FILES['avatar']  # 获取上传的文件
        title = request.POST.get('title')  # 获取文件标题（名称）
        user_id = request.POST.get('userId')
        print(user_id)
        user = User.objects.get(student_id=user_id)
        
        # 检查文件类型
        if not allowed_file(avatar.name):
            return JsonResponse({"message": "不支持的文件类型"}, status=400)

        # 为文件生成唯一的文件名
        timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        filename = avatar.name  # 直接使用文件名
        local_path = os.path.join(settings.MEDIA_ROOT, f"avatars/{timestamp}_{filename}")  # 本地保存路径

        # 确保保存路径存在
        os.makedirs(os.path.dirname(local_path), exist_ok=True)

        # 将文件保存到本地
        with default_storage.open(local_path, 'wb+') as temp_file:
            for chunk in avatar.chunks():
                temp_file.write(chunk)

        # 上传到腾讯云
        try:
            file_url = upload(local_path, filename)  # 使用你写的 upload 方法上传图片并获取图床URL

            # 上传完毕后删除本地文件
            os.remove(local_path)
            user.avatar = file_url
            user.save()
            # 返回上传成功和图床URL
            return JsonResponse({
                "message": "文件上传成功",
                "file_name": filename,
                "url": file_url  # 返回图床URL
            })

        except Exception as e:
            # 上传失败处理
            return JsonResponse({"message": "上传失败", "error": str(e)}, status=500)

    # 如果没有文件上传
    return JsonResponse({"message": "无文件上传"}, status=400)