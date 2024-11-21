from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from myapp2.models import UserProfile

import json,random
@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        student_number = data.get('studentNumber')
        password = data.get('password')
        user = authenticate(username=student_number, password=password)
        if user is not None:
            try:
                urls = user.profile.urls  # 访问 UserProfile 的 urls 属性
            except UserProfile.DoesNotExist:
                 gender = random.choice(['women', 'men'])
                 number = random.randint(0, 99)
                 urls = f"https://randomuser.me/api/portraits/{gender}/{number}.jpg"

            return JsonResponse({
                "success": True,
                "message": "登录成功",
                "urls": urls
            })
        else:
            return JsonResponse({"success": False, "message": "用户名或密码错误"}, status=401)
    return JsonResponse({"error": "请求方法错误"}, status=405)

@csrf_exempt  # 如果没有启用 CSRF 保护，可以用此装饰器（生产环境应避免）
def register_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            student_number = data.get('studentNumber')
            college = data.get('college')
            email = data.get('email')
            entry_year = data.get('entryYear')
            password = data.get('password')
            confirm_password = data.get('confirmPassword')
            gender = random.choice(['women', 'men'])
            number = random.randint(0, 99)
            urls = f"https://randomuser.me/api/portraits/{gender}/{number}.jpg"

            if User.objects.filter(username=student_number).exists():
                return JsonResponse({"success": False, "message": "该学号已注册"}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({"success": False, "message": "该邮箱已注册"}, status=400)

            user = User.objects.create_user(
                username=student_number,
                email=email,
                password=password,
                first_name=name
            )

            user.profile.urls = urls
            user.profile.save()

            return JsonResponse({"success": True, "message": "注册成功"}, status=201)

        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)
    return JsonResponse({"error": "请求错误"}, status=405)
