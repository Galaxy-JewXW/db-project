from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from learingCompanionInBeihang.settings import MEDIA_ROOT, STATIC_URL
from learingCompanionInBeihang.apps.users.models import User
from learingCompanionInBeihang.apps.utils.views import check_role, response_json, decode_request
from learingCompanionInBeihang.apps.utils.constants import ImageErrorCode, UserRole
from .upload_images import upload

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


class UploadUserAvatar(APIView):
    def post(self, request):
        try:
            # 获取用户 ID
            # data = decode_request(request)
            user_id = request.data.get('user_id')
            user = User.objects.get(id=user_id)
            print(User.objects.all())
            print(user_id)
            print(user)
            # 获取图片文件
            print(request.data)
            print(request.FILES)
            img = request.FILES.get('img')
            if not img:
                return Response({"error": "No image file provided."}, status=HTTP_400_BAD_REQUEST)

            # 截取文件后缀和文件名
            img_name = img.name
            mobile = os.path.splitext(img_name)[0]
            ext = os.path.splitext(img_name)[1]

            # 定义保存的文件名
            img_name = f'avatar-{mobile}{ext}'

            # 定义本地临时保存路径
            temp_dir = os.path.join(STATIC_URL, user.student_id + "avatar")  # 创建临时上传文件夹
            os.makedirs(temp_dir, exist_ok=True)
            img_path = os.path.join(temp_dir, img_name)

            # 写入文件到本地
            with open(img_path, 'wb') as fp:
                for chunk in img.chunks():
                    fp.write(chunk)

            # 上传到 COS
            url = upload(img_path, img_name)

            # 更新用户头像
            user.avatar = url
            user.save()

            # 删除本地临时文件
            if os.path.exists(img_path):
                os.remove(img_path)

            return Response({
                "success": True,
                "message": "上传成功",
                "avatar_url": url
            }, status=HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"Upload failed: {str(e)}"}, status=HTTP_400_BAD_REQUEST)


class UploadUserImage(APIView):
    def post(self, request):
        try:
            img = request.FILES.get('img')
            if not img:
                return Response({"error": "No image file provided."}, status=HTTP_400_BAD_REQUEST)

            # 截取文件后缀和文件名
            img_name = img.name
            mobile = os.path.splitext(img_name)[0]
            ext = os.path.splitext(img_name)[1]

            # 定义保存的文件名
            img_name = f'img-{mobile}{ext}'

            # 定义本地临时保存路径
            temp_dir = os.path.join(STATIC_URL, img_name)  # 创建临时上传文件夹
            os.makedirs(temp_dir, exist_ok=True)
            img_path = os.path.join(temp_dir, img_name)

            # 写入文件到本地
            with open(img_path, 'wb') as fp:
                for chunk in img.chunks():
                    fp.write(chunk)


            # 上传到 COS
            url = upload(img_path, img_name)

            # 删除本地临时文件
            if os.path.exists(img_path):
                os.remove(img_path)

            return Response({
                "success": True,
                "message": "上传成功",
                "img_url": url
            }, status=HTTP_200_OK)

        except Exception as e:
            return Response({"error": f"Upload failed: {str(e)}"}, status=HTTP_400_BAD_REQUEST)
