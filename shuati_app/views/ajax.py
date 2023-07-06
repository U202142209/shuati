# encoding: utf-8
'''
 @author: 我不是大佬 
 @contact: 2869210303@qq.com
 @wx; safeseaa
 @qq; 2869210303
 @file: ajax.py
 @time: 2023/7/1 19:29
  '''
import random

from django.db.models import Subquery
from django.http import JsonResponse
from .adminsite import setError, setSuccess
from ..config.config import main, get_first_15_chars
from ..models import Tag, User, Question, AnswerRecord


# 发送邮箱颜验证码
def getemailcode(request):
    email = request.GET.get("email")
    print("输入的邮箱是；", email)

    code = main(email)
    if code:
        request.session["email"] = email
        request.session['email_login_code'] = code
        request.session.set_expiry(60 * 5)
        data_dict = {"status": True, "msg": "成功向邮箱；" + email + "发送了验证码，请在5分钟内输入正确的验证码完成验证。"}
    else:
        data_dict = {"status": False, "msg": "验证码发送失败，请确认 " + email + " 是否为有效的邮箱地址"}
    return JsonResponse(data_dict)


def getAllTags(request):
    tags = Tag.objects.filter(
        is_delete=0
    )
    if tags:
        data_dict = {
            "code": 200,
            "status": True,
            "msg": "获取题目分类成功",
            "data": []
        }
        for tag in tags:
            data_dict["data"].append(
                {
                    "tag": tag.tag,
                    "create_time": tag.create_time
                }
            )
        return JsonResponse(data_dict)
    return JsonResponse({
        "code": 500,
        "status": False,
        "data": [],
        "msg": "没有查询到数据"
    })


def getRandomQuestion(request):
    if not request.session.get("username"):
        return setError("没有登录，无权访问")
    # 验证用户邮箱是否合格
    c1 = (request.session.get("username", "1") != request.GET.get("username", "2"))
    c2 = (request.session.get("email", "1") != request.GET.get("email", "2"))
    if c1 or c2:
        return setError("用户身份校验未通过，获取题目信息失败")

    # 判断是否携带标签
    if not Question.objects.filter(
            tag__nid=request.GET.get("tag_nid", ""),
            tag__tag=request.GET.get("tag_tag", ""),
            is_delete=False
    ).exists():
        return setError("此标签暂时没有题目，等待管理员添加中...")

    # 获取用户的邮箱
    email = request.session.get("email")
    # 获取用户对象
    user = User.objects.get(email=email)
    # 使用子查询获取用户已经回答过的题目的id列表
    answered_questions = AnswerRecord.objects.filter(
        user=user,
        question__tag__tag=request.GET.get("tag_tag"),
        question__tag__nid=request.GET.get("tag_nid")
    ).values_list('question__question_id', flat=True)
    # 输出已经写过的题目，测试
    # print("answered_questions")
    # for i in answered_questions:
    #     print(i)

    # 查询用户没有回答过的题目
    q = Question.objects.exclude(
        question_id__in=answered_questions). \
        filter(
        is_delete=False,
        tag__tag=request.GET.get("tag_tag"),
        tag__nid=request.GET.get("tag_nid")
    )
    if not q:
        return setError("此标签的题目已经全部被您刷完啦！去其他的分类看看吧")
    q = q[random.randint(0, len(q) - 1)]
    return setSuccess(
        msg="获取题目成功",
        data={
            "question_id": q.question_id,
            "question_content": q.question_content,
            "options": q.options,
            "create_time": q.create_time
        }
    )


# 提交答案
def submitAnswer(request):
    # 判断用户是否登录，否则无权访问此接口
    if not request.session.get("username"):
        return setError("没有登录，无权访问")
    # 是否提交了答案
    if not request.GET.get("answer"):
        return setError("请提交有效的答案")
    # 校验是否为有效的用户
    curuser = User.objects.filter(is_delete=False, username=request.session.get("username", ""),
                                  email=request.session.get("email", "")).first()
    if not curuser:
        return setError("用户校验失败，无法提交答案")
    # 校验是否为有效的题目
    q = Question.objects.filter(
        is_delete=False, question_id=request.GET.get("question_id", "1")).first()
    if not q:
        return setError("question_id不存在")
    # 判断是否已经写过了这道题目
    if AnswerRecord.objects.filter(
            is_delete=False,
            user=curuser,
            question=q).exists():
        return setError("这道题你已经写过了，无法再次提交")
    # 添加答题记录
    AnswerRecord.objects.create(user=curuser, question=q, answer=request.GET.get("answer"),
                                is_correct=(request.GET.get("answer") == q.correct_answer))
    # 提交成功，返回结果
    return setSuccess(
        msg="提交成功",
        data={
            "result": (request.GET.get("answer") == q.correct_answer),
            "question_id": q.question_id,
            "correct_answer": q.correct_answer,
            "my_answer": request.GET.get("answer"),
            "answer_detail": q.answer_detail,
        }
    )


# 获答题记录
def getRecord(request):
    # 判断用户是否登录，否则无权访问此接口
    if (not request.session.get("username")) or (not request.session.get("email")):
        return setError("没有登录，无权访问")
    # 验证用户邮箱是否合格
    if (request.session.get("username", "1") != request.GET.get("username", "2")) or (
            request.session.get("email", "1") != request.GET.get("email", "2")):
        return setError("用户身份校验未通过，获取题目信息失败")
    user = User.objects.filter(
        is_delete=False,
        email=request.session.get("email"),
        username=request.session.get("username")
    ).first()
    if not user:
        return setError("用户信息核对失败，无法获取数据")
    try:
        page = int(request.GET.get("page"))
        if page <= 0:
            page = 1
    except:
        page = 1
    print((request.GET.get("isfinderrorbook", "0") == 1))
    if (request.GET.get("isfinderrorbook", "0") == "1"):
        recoeds = AnswerRecord.objects.filter(
            is_delete=False, user=user,
            question__question_content__contains=request.GET.get("keywords", ""),
            isInErrorBook=True
        ).order_by("-create_time")
    else:
        recoeds = AnswerRecord.objects.filter(
            is_delete=False, user=user,
            question__question_content__contains=request.GET.get("keywords", ""),
        ).order_by("-create_time")
    if not recoeds:
        return setError("没有查询到数据")
    recordData = []
    length = len(recoeds)
    recoeds = recoeds[(page - 1) * 10: page * 10]
    for r in recoeds:
        recordData.append({
            "is_correct": r.is_correct,
            "create_time": r.create_time,
            "answer": r.answer,
            "question_id": r.question.question_id,
            "question_content": r.question.question_content,
            "correct_answer": r.question.correct_answer,
            "tag": r.question.tag.tag,
            "options": r.question.options,
            "answer_detail": r.question.answer_detail,
            "answer_num": r.question.answer_num(),
            "correctPercent": r.question.correctPercent(),
            "isInErrorBook": r.isInErrorBook,
        })
    return setSuccess(
        msg="获取答题记录信息成功!",
        data=recordData,
        len=length

    )


def getDetailData(request):
    if (not request.session.get("username")) or (not request.session.get("email")):
        return setError("没有登录，无权访问")
    user = User.objects.filter(
        is_delete=False,
        email=request.session.get("email"),
        username=request.session.get("username")
    ).first()
    if not user:
        return setError("用户身份校验失败，无法获取数据")
    return setSuccess(
        msg="获取数据成功！",
        data={
            "username": user.username,
            "email": user.email,
            "detail": user.detail,
            "totalQuestionNum": user.totalQuestionNum(),
            "totalCorrectNum": user.totalCorrectNum(),
            "totalCorrectPercentage": user.totalCorrectPercentage,

        })


def addintoErrorBook(request):
    if (not request.session.get("username")) or (not request.session.get("email")):
        return setError("没有登录，无权访问")
    user = User.objects.filter(
        is_delete=False,
        email=request.session.get("email"),
        username=request.session.get("username")
    ).first()
    if not user:
        return setError("用户身份校验失败，无法获取数据")
    record = AnswerRecord.objects.filter(
        is_delete=False,
        user=user,
        question__question_id=request.GET.get("question_id"),
    ).first()
    if not record:
        return setError("警告，异常操作")
    record.isInErrorBook = True
    record.save()
    return setSuccess(msg="加入错题本成功！")


def removefromErrorBook(request):
    if (not request.session.get("username")) or (not request.session.get("email")):
        return setError("没有登录，无权访问")
    user = User.objects.filter(
        is_delete=False,
        email=request.session.get("email"),
        username=request.session.get("username")
    ).first()
    if not user:
        return setError("用户身份校验失败，无法获取数据")
    record = AnswerRecord.objects.filter(
        is_delete=False,
        user=user,
        question__question_id=request.GET.get("question_id"),
    ).first()
    if not record:
        return setError("警告，异常操作")
    record.isInErrorBook = False
    record.save()
    return setSuccess("移出错题本成功！")
