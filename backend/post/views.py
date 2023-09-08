import json

from django.http import JsonResponse
from django.views.decorators.http import require_POST

from post import controllers
from utils.jwt import login_required
from utils.post_params_check import post_params_check
from utils.reply_post_params_check import reply_post_params_check


@login_required
def post_list(request):
    if request.method == "GET":
        page = int(request.GET.get("page", 1))
        size = int(request.GET.get("size", 10))
        user_id = request.GET.get("userId", 0)
        order_by_reply = bool(request.GET.get("orderByReply", False))

        post_list, count, result = controllers.get_post_list(
            user_id, page, size, order_by_reply
        )
        if result:
            return JsonResponse(
                {
                    "posts": post_list,
                    "page": page,
                    "size": size,
                    "total": count,
                },
                status=200,
            )
        else:
            return JsonResponse({"message": "error"}, status=500)

    elif request.method == "POST":
        try:
            content = json.loads(request.body)
            if not content:
                return JsonResponse({"message": "bad arguments"}, status=400)

            key, passed = post_params_check(content)
            if not passed:
                return JsonResponse(
                    {"message": "invalid arguments: " + key}, status=400
                )

            id, result = controllers.create_post(
                content["title"], content["content"], request.user.id
            )

            if result:
                return JsonResponse(
                    {"postId": id, "message": "ok"}, status=200
                )
            else:
                return JsonResponse({"message": "error"}, status=500)
        except KeyError:
            return JsonResponse({"message": "bad arguments"}, status=400)

    else:
        return JsonResponse({"message": "error"}, status=500)


@login_required
def post_detail(request, postId):
    if request.method == "GET":
        detail, result = controllers.get_post_detail(postId)
        if result:
            return JsonResponse(detail, status=200)
        else:
            return JsonResponse({"message": "error"}, status=500)

    elif request.method == "PUT":
        try:
            content = json.loads(request.body)
            if not content:
                return JsonResponse({"message": "bad arguments"}, status=400)

            key, passed = post_params_check(content)
            if not passed:
                return JsonResponse(
                    {"message": "invalid arguments: " + key}, status=400
                )

            check = controllers.check_post(postId, request.user.id)
            if not check:
                return JsonResponse({"message": "not found"}, status=404)

            result = controllers.update_post(
                content["title"], content["content"], postId, request.user.id
            )

            if result:
                return JsonResponse({"message": "ok"}, status=200)
            else:
                return JsonResponse({"message": "error"}, status=500)
        except KeyError:
            return JsonResponse({"message": "bad arguments"}, status=400)

    else:
        return JsonResponse({"message": "error"}, status=500)


@require_POST
@login_required
def reply_post(request, postId):
    try:
        content = json.loads(request.body)
        if not content:
            return JsonResponse({"message": "bad arguments"}, status=400)

        key, passed = reply_post_params_check(content)
        if not passed:
            return JsonResponse(
                {"message": "invalid arguments: " + key}, status=400
            )

        if "replyId" in content:
            reply_id = content["replyId"]
            check = controllers.check_reply(postId, reply_id)
            if not check:
                return JsonResponse({"message": "not found"}, status=404)
        else:
            reply_id = 0

        result = controllers.create_reply(
            content["content"], request.user.id, postId, reply_id
        )

        if result:
            return JsonResponse({"message": "ok"}, status=200)
        else:
            return JsonResponse({"message": "error"}, status=500)
    except KeyError:
        return JsonResponse({"message": "bad arguments"}, status=400)


@login_required
def modify_reply(request, postId, replyId):
    try:
        content = json.loads(request.body)
        if not content:
            return JsonResponse({"message": "bad arguments"}, status=400)

        key, passed = reply_post_params_check(content)
        if not passed:
            return JsonResponse(
                {"message": "invalid arguments: " + key}, status=400
            )

        check = controllers.check_self_reply(replyId, request.user.id)
        if not check:
            return JsonResponse({"message": "not found"}, status=404)

        result = controllers.update_reply(
            content["content"], request.user.id, postId, replyId
        )

        if result:
            return JsonResponse({"message": "ok"}, status=200)
        else:
            return JsonResponse({"message": "error"}, status=500)
    except KeyError:
        return JsonResponse({"message": "bad arguments"}, status=400)
