import json

from django.db.models import Model
from django.http import HttpResponse, JsonResponse

from user import controllers
from utils.jwt import encrypt_password, generate_jwt, login_required
from utils.register_params_check import register_params_check


@login_required
def get_user_info(request):
    """
    获取当前登录用户信息
    """
    user = request.user
    return JsonResponse(
        {
            "id": user.id,
            "username": user.username,
            "nickname": user.nickname,
            "created": user.created,
            "url": user.url,
            "mobile": user.mobile,
        }
    )


@login_required
def get_user_info_by_id(request, userId):
    """
    获取指定用户信息
    """
    try:
        user, result = controllers.get_user(userId)
        if result:
            return JsonResponse(
                {
                    "id": user.id,
                    "nickname": user.nickname,
                    "created": user.created,
                }
            )
        else:
            return JsonResponse({"message": user}, status=500)
    except Model.DoesNotExist:
        return JsonResponse({"message": "User not found"}, status=404)


def login(request):
    """
    登录
    """
    if request.method == "OPTIONS":
        return HttpResponse(status=204)

    if request.method != "PATCH":
        return JsonResponse({"message": "Method not allowed"}, status=405)

    try:
        content = json.loads(request.body)
        username = content.get("username")
        password = content.get("password")

        user, result = controllers.get_user_with_pass(
            username=username, password=encrypt_password(password)
        )
        if result:
            jwt = generate_jwt({"user_id": user.id, "nickname": user.nickname})
            return JsonResponse(
                {
                    "jwt": jwt,
                    "userId": user.id,
                    "username": user.username,
                    "nickname": user.nickname,
                }
            )
        else:
            return JsonResponse({"message": "Invalid credentials"}, status=401)
    except json.JSONDecodeError:
        return JsonResponse({"message": "bad arguments"}, status=400)
    except:
        return JsonResponse({"message": "bad arguments"}, status=400)


def logout(request):
    """
    登出
    本次作业中简化，不做任何操作
    """
    return JsonResponse({"message": "ok"})


def register_user(request):
    """
    用户注册
    """
    if request.method != "POST":
        return JsonResponse({"message": "Method not allowed"}, status=405)

    try:
        print(request.body)
        content = json.loads(request.body)
        username = content.get("username")
        password = content.get("password")
        nickname = content.get("nickname")
        url = content.get("url")
        mobile = content.get("mobile")
        magic_number = content.get("magic_number")

        key, passed = register_params_check(content)
        if not passed:
            return JsonResponse(
                {"message": f"Invalid arguments: {key}"}, status=400
            )

        result = controllers.create_user(
            username=username,
            password=encrypt_password(password),
            nickname=nickname,
            url=url,
            mobile=mobile,
            magic_number=magic_number,
        )
        if result:
            return JsonResponse({"message": "ok"}, status=200)
        else:
            return JsonResponse({"message": "Error"}, status=500)
    except json.JSONDecodeError:
        return JsonResponse({"message": "bad arguments"}, status=400)
    except:
        return JsonResponse({"message": "bad arguments"}, status=400)
