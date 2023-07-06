# encoding: utf-8
'''
 @author: 我不是大佬 
 @contact: 2869210303@qq.com
 @wx; safeseaa
 @qq; 2869210303
 @file: adminsite.py
 @time: 2023/7/1 23:03
  '''
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render  # 导出render方法
from django.utils.timezone import localtime  # 导出localtime方法

from ..config.config import get_nid, get_first_15_chars
from ..models import AdminUser, Tag, Question


def adminlogin(request):
    if request.session.get("admin_username", None):
        return redirect("/shuati_app/adminconsole")
    if request.method == "GET":
        return render(request, "adminsite/adminlogin.html")
    username = request.POST.get("username", "")
    password = request.POST.get("password", "")
    if AdminUser.objects.filter(
            username=username,
            password=password
    ).exists():
        request.session["admin_username"] = username
        request.session["is_admin"] = True
        request.session["is_logined"] = True
        return redirect("/shuati_app/adminconsole/")
    return render(request, "adminsite/adminlogin.html", {
        "msg": "用户名或者密码不正确"
    })


def adminconsole(request):
    if not request.session.get("admin_username", None):
        return redirect("/shuati_app/adminlogin?msg=无权访问")
    return render(request, "adminsite/adminconsole.html")


def adminlogout(request):
    request.session.clear()
    return redirect("/shuati_app/adminlogin/?message=退出登录成功！")


def setError(msg):
    return JsonResponse({
        "code": 500,
        "status": False,
        "msg": msg,
        "data": [],
        "len": 0
    }, content_type="application/json")


def setSuccess(msg, data=None, len=0):
    return JsonResponse({
        "code": 200,
        "status": True,
        "msg": msg,
        "data": data,
        "len": len
    }, content_type="application/json")


def admin_addneewtag(request):
    if not request.session.get("admin_username", None):
        return setError("不是管理员，无权操作")
    tagname = request.GET.get("tagname")
    if not tagname:
        return setError("输入的标签名不能为空")
    if Tag.objects.filter(
            tag=tagname,
            is_delete=False
    ).exists():
        return setError(f"题目分类标签 {tagname} 已经存在，无法继续添加")
    try:
        tag = Tag.objects.create(
            tag=tagname.strip(),
            nid=get_nid()
        )
        return setSuccess("新增题目分类标签成功")
    except Exception as error:
        return setError("发生了错误：" + str(error))


def admin_selecttag(request):
    # if not request.session.get("admin_username", None):
    #     return setError("不是管理员，无权操作")
    # 查询的关键字，模糊查询
    tagname = request.GET.get("tagname", "")
    # 查询的页数,每页10条数据，page从1开始
    try:
        page = int(request.GET.get("page"))
        if page <= 0:
            page = 1
    except:
        page = 1
    tags = Tag.objects.filter(
        tag__contains=tagname.strip(),
        is_delete=False
    ).order_by('-create_time').all()
    if tags:
        length = len(tags)
        tags = tags[(page - 1) * 10: page * 10]
        data = []
        for tag in tags:
            data.append({
                "tag": tag.tag,
                "create_time": localtime(tag.create_time),
                "nid": tag.nid,
                "question_num":tag.get_question_num()
            })
        return setSuccess(
            msg="查询题目标签数据成功",
            data=data,
            len=length
        )
    return setError("没有查询到数据")


def admin_deletetag(request):
    if not request.session.get("admin_username", None):
        return setError("不是管理员，无权操作")
    tagname = request.GET.get("tagname")
    nid = request.GET.get("nid")
    tags = Tag.objects.filter(
        tag=tagname,
        nid=nid,
        is_delete=False
    ).first()
    if not tags:
        return setError("没有查询到此数据，无法删除")
    tags.is_delete = True
    tags.save()
    return setSuccess("删除成功")


def admin_edit_tag(request):
    if not request.session.get("admin_username", None):
        return setError("不是管理员，无权操作")
    tagname = request.GET.get("tagname")
    nid = request.GET.get("nid")
    tag = Tag.objects.filter(
        nid=nid,
        is_delete=False
    ).first()
    if not tag:
        return setError("没有查询到此数据，修改失败")
    tag.tag = tagname
    tag.save()
    return setSuccess("修改题目标签成功")


def admin_getAllTagsName(request):
    if not request.session.get("admin_username", None):
        return setError("不是管理员，无权操作")
    tags = Tag.objects.filter(is_delete=False).order_by('-create_time').all()
    if not tags:
        return setError("没有任何标签，请先去添加标签再新增题目")
    data = []
    for tag in tags:
        data.append({
            "tag": tag.tag,
            "nid": tag.nid
        })
    return setSuccess(
        msg="查询标签成功",
        data=data
    )


def admin_add_question(request):
    if not request.session.get("admin_username", None):
        return setError("不是管理员，无权操作")
    try:
        if Question.objects.filter(
                is_delete=False,
                question_content=request.GET.get("questionContent")
        ).exists():
            return setError("该题目已经存在，不可再次添加，题目问题不可重复")
        question = Question(question_id=get_nid())
        optionsdata = {}
        for key, value in request.GET.items():
            if key == "questionContent":
                question.question_content = value.strip()
            elif key == "questionCategory":
                question.tag = Tag.objects.filter(
                    tag=value,
                    is_delete=False
                ).first()
            elif key == "correctAnswer":
                question.correct_answer = value
            elif key.startswith("option"):
                optionsdata[key[-1]] = value.strip()
        question.options = optionsdata
        question.answer_detail = request.GET.get("answer_detail", "")
        question.save()
        return setSuccess("新增问题信息成功！")
    except Exception as error:
        print(error)
        return setError("系统发生了错误，新增题目信息失败，原因：" + str(error))


def admin_select_question(request):
    if not request.session.get("admin_username", None):
        return setError("不是管理员，无权操作")
    try:
        page = int(request.GET.get("page"))
        if page <= 0:
            page = 1
    except:
        page = 1
    questions = Question.objects.filter(
        question_content__contains=request.GET.get("question_content", "").strip(),
        tag__tag__contains=request.GET.get("tagname", ""),
        is_delete=False,
    ).order_by('-create_time').all()
    if questions:
        length = len(questions)
        questions = questions[(page - 1) * 10: page * 10]
        qdata = []
        for q in questions:
            qdata.append({
                "question_id": q.question_id,
                "question_content": get_first_15_chars(q.question_content),
                "tag": q.tag.tag,
                "answer_num": q.answer_num(),
                "create_time": localtime(q.create_time)
            })
        return setSuccess(
            msg="查询问题信息成功",
            data=qdata,
            len=length
        )
    return setError("依次此条件，没有查询到题目信息")

def admin_getQuestionByNid(request):
    question_id=request.GET.get("question_id")
    q=Question.objects.filter(
        question_id=question_id,
        is_delete=False
    ).first()
    if q:
        return setSuccess(
            msg="查询问题成功",
            data={
                "question_id":q.question_id,
                "question_content":q.question_content,
                "options":q.options,
                "correct_answer":q.correct_answer,
                "tag":q.tag.tag,
                "answer_detail":q.answer_detail,
                "answer_num":q.answer_num(),
                "create_time":localtime(q.create_time)
            }
        )
    return setError("没有查询到数据")

def admin_deleteQuestion(request):
    if not request.session.get("admin_username", None):
        return setError("不是管理员，无权操作")
    q = Question.objects.filter(
        question_id=request.GET.get("question_id","error"),
        is_delete=False
    ).first()
    if q:
        q.is_delete=True
        q.save()
        return setSuccess("删除题目成功！")
    return setError("没有查询到此题目信息，删除失败")