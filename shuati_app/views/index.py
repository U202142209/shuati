# encoding: utf-8
'''
 @author: 我不是大佬 
 @contact: 2869210303@qq.com
 @wx; safeseaa
 @qq; 2869210303
 @file: index.py
 @time: 2023/7/1 16:03
  '''

from io import BytesIO
from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import View

from ..config.config import get_verified_image
from ..config.forms import LoginRegisterForm
from ..models import User, Tag, AnswerRecord, Question


def shuati_app_index(request):
    return render(request, "index.html")


class LoginView(View):
    """类视图：处理注册"""

    def get(self, request):
        if request.session.get('info'):  # 如果已经登录，直接跳转到控制台
            return redirect('/student_console/')
        """处理GET请求，返回注册页面"""
        return render(request, 'login.html')

    def post(self, request):
        """处理POST请求，实现注册逻辑"""
        if not request.session.get("email", None):
            return render(
                request, 'login.html',
                {
                    "msg": "请点击获取邮箱验证码",
                }
            )
        code = request.POST.get("code", "")
        if code != request.session.get("email_login_code", ""):
            return render(
                request, 'login.html',
                {
                    "msg": "输入的邮箱验证码不正确",
                    "email": request.session.get("email")
                }
            )
        curuser = User.objects.filter(
            email=request.session.get("email")
        ).first()
        if not curuser:
            curuser=User.objects.create(
                username=request.session.get("email"),
                email=request.session.get("email")
            )
        request.session["is_logined"] = True
        request.session["email"] = curuser.email
        request.session["username"] = curuser.username
        # 三天免登录
        request.session.set_expiry(60 * 60 * 24 * 3)
        return redirect("/shuati_app/")

def get_captcha(request):
    image, verify = get_verified_image()
    stream = BytesIO()
    image.save(stream, 'png')

    request.session["image_code"] = verify
    # 验证码 60 秒内有效
    request.session.set_expiry(300)
    return HttpResponse(stream.getvalue())


# 退出登录
def logout(request):
    request.session.clear()
    return redirect("/shuati_app/login/?message=退出登录成功！")


def returnErrorPage(request, msg="没有登录，无权访问."):
    return render(request, 'error.html', {
        "msg": msg
    })


def tagdetail(request):
    if not request.session.get("username"):
        return returnErrorPage(request)
    tagid = request.GET.get("tagid")
    tag = Tag.objects.filter(
        nid=tagid,
        is_delete=False
    ).values('tag', 'nid').first()
    if not tag:
        return returnErrorPage(request, "没有查询此标签，无法访问")
    return render(request, "tagdetail.html", {
        "tag_nid": tag["nid"],
        "tag_tag": tag["tag"],
        "user_username": request.session.get("username"),
        "user_email": request.session.get("email")
    })


def record(request):
    if not request.session.get("username"):
        return returnErrorPage(request)
    user = User.objects.filter(
        is_delete=False,
        email=request.session.get("email", ""),
        username=request.session.get("username", "1")
    ).first()
    if not user:
        return returnErrorPage(request, msg="用户身份校验失败，无法访问")
    return render(request, "user/answerrecord.html", {
        "user_username": request.session.get("username"),
        "user_email": request.session.get("email"),
        "totalQuestionNum": user.totalQuestionNum(),
        "totalCorrectPercentage": user.totalCorrectPercentage()
    })


def testpage(request):
    return render(request, "testpage.html")
