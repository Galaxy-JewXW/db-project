from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from users.models import User
from django.contrib.auth import authenticate

import json,random
@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        student_number = data.get('studentNumber')
        password = data.get('password')

        try:
            # 验证用户
            user = User.objects.get(student_id=student_number, password_digest=password)
        except User.DoesNotExist:
            return JsonResponse({"success": False, "message": "用户名或密码错误"}, status=401)

        # 返回用户信息
        return JsonResponse({
            "success": True,
            "message": "登录成功",
            "urls": user.avatar or f"https://randomuser.me/api/portraits/{random.choice(['women', 'men'])}/{random.randint(0, 99)}.jpg",
            "name": user.name,
            "role": user.user_role,
            "entry_year": user.entryYear,
            "college": user.college,
            "email": user.mail
        })

    return JsonResponse({"error": "请求方法错误"}, status=405)
@csrf_exempt
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

            # 检查密码是否一致
            if password != confirm_password:
                return JsonResponse({"success": False, "message": "两次密码不一致"}, status=400)

            # 检查学号是否已注册
            if User.objects.filter(student_id=student_number).exists():
                return JsonResponse({"success": False, "message": "该学号已注册"}, status=400)

            # 检查邮箱是否已注册
            if User.objects.filter(mail=email).exists():
                return JsonResponse({"success": False, "message": "该邮箱已注册"}, status=400)

            # 创建用户
            gender = random.choice(['women', 'men'])
            number = random.randint(0, 99)
            avatar = f"https://randomuser.me/api/portraits/{gender}/{number}.jpg"

            user = User.objects.create(
                student_id=student_number,
                name=name,
                password_digest=password,  # 存储密码（建议加密）
                mail=email,
                college=college,
                entryYear=entry_year,
                avatar=avatar,
                user_role=0  # 默认角色
            )

            return JsonResponse({"success": True, "message": "注册成功"}, status=201)

        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)

    return JsonResponse({"error": "请求错误"}, status=405)