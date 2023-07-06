# encoding: utf-8
'''
 @author: 我不是大佬 
 @contact: 2869210303@qq.com
 @wx; safeseaa
 @qq; 2869210303
 @file: urls.py
 @time: 2023/7/1 15:48
  '''

from django.urls import re_path as url
from django.urls import re_path, path, include
from .views import index, ajax,adminsite

urlpatterns = [
    url(r'^$', index.shuati_app_index, name="index"),
    path("login/", index.LoginView.as_view(), name="login"),
    path('get_captcha/', index.get_captcha, name="get_captcha"),
    # 获取邮箱验证码
    path('getemailcode/', ajax.getemailcode, name="getemailcode"),
    # 退出登录
    path("logout/", index.logout, name="logout"),
    # 获取所有的标签
    path("getAllTags/",ajax.getAllTags,name="getAllTags"),
    # 管理员登录
    path("adminlogin/",adminsite.adminlogin,name="adminlogin"),
    # 管理员后天
    path("adminconsole/",adminsite.adminconsole,name="adminconsole"),
    path("adminlogout/",adminsite.adminlogout,name="adminlogout"),
    # 新增题目分类标签
    path("admin_addneewtag/",adminsite.admin_addneewtag,name="admin_addneewtag"),
    # 查询题目分类标签
    path("admin_selecttag/",adminsite.admin_selecttag,name="admin_selecttag"),
    # 删除题目标签数据
    path("admin_deletetag/",adminsite.admin_deletetag,name="admin_deletetag"),
    # 编辑标签
    path("admin_edit_tag/",adminsite.admin_edit_tag,name="admin_edit_tag"),
    # 查询所有标签名称
    path("admin_getAllTagsName/",adminsite.admin_getAllTagsName,name="admin_getAllTagsName"),
    # 新增问题
    path("admin_add_question/",adminsite.admin_add_question,name="admin_add_question"),
    # 查询问题
    path("admin_select_question/",adminsite.admin_select_question,name="admin_select_question"),
    # 按照id查询问题
    path("admin_getQuestionByNid/",adminsite.admin_getQuestionByNid,name="admin_getQuestionByNid"),
    # 删除题目
    path("admin_deleteQuestion",adminsite.admin_deleteQuestion,name="admin_deleteQuestion"),
    # 标签详情页面
    path("tagdetail/",index.tagdetail,name="tagdetail"),
    # 根据用户获取没有写过的题目
    path("getRandomQuestion/",ajax.getRandomQuestion,name="getRandomQuestion"),
    # 提交答案，返回结果
    path("submitAnswer/",ajax.submitAnswer,name="submitAnswer"),
    # 答题记录
    path("record/",index.record,name="record"),
    # 获取记录信息
    path("getRecord/",ajax.getRecord,name="getRecord"),
    # 获取数据
    path("getDetailData/",ajax.getDetailData,name="getDetailData"),
    # 测试页面
    path("testpage/",index.testpage,name="testpage"),
    # 加入收藏
    path("addintoErrorBook/",ajax.addintoErrorBook,name="addintoErrorBook"),
    path("removefromErrorBook/",ajax.removefromErrorBook,name="removefromErrorBook"),

]
