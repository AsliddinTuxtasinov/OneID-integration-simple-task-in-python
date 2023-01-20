import os
from django.http import HttpResponse
from django.shortcuts import redirect, render
from dotenv import load_dotenv

from auusers.utils import get_access_token, get_user_info, logout_util

load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
scope = os.getenv('Scope')
redirect_uri = os.getenv('REDIRECT_URI')
state = os.getenv('STATE')


def get_code(request):
    return redirect(
        to=f"{os.getenv('BASE_URL')}?response_type=one_code&client_id={client_id}&redirect_uri={redirect_uri}&Scope={scope}&state={state}"
    )


def login(request):
    code = request.GET.get('code')
    if code is None:
        return HttpResponse("Code None")

    res, access_token = get_access_token(code=code, client_id=client_id, client_secret=client_secret)
    user_info = get_user_info(access_token=access_token, client_id=client_id, client_secret=client_secret, scope=scope)

    request.session['code'] = code
    context = {
        "is_authenticate": True,
        "additional": res,
        "user_info": user_info
    }
    return render(request, "index.html", context)


def profile(request):
    code = request.session.get('code')
    if code is None:
        return HttpResponse("404")

    res, access_token = get_access_token(code=code, client_id=client_id, client_secret=client_secret)
    user_info = get_user_info(access_token=access_token, client_id=client_id, client_secret=client_secret, scope=scope)
    data = {
        "additional": res,
        "user_info": user_info,
        "is_authenticate": True
    }
    return render(request, "list.html", data)


def logout(request):
    code = request.session.get('code')
    if code is None:
        return HttpResponse("Code None")

    res, access_token = get_access_token(code=code, client_id=client_id, client_secret=client_secret)
    logout_util(client_id=client_id, client_secret=client_secret, access_token=access_token, scope=scope)

    del request.session['code']
    request.session.modified = True

    context = {
        "is_authenticate": False
    }
    return render(request, "index.html", context)


def index(request):
    code = request.session.get('code')

    context = {}
    if code is None:
        context["is_authenticate"] = False
    else:
        _, access_token = get_access_token(code=code, client_id=client_id, client_secret=client_secret)
        user_info = get_user_info(access_token=access_token, client_id=client_id, client_secret=client_secret, scope=scope)
        context["is_authenticate"] = True
        context["user_info"] = user_info

    return render(request, "index.html", context)
