import re
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render, HttpResponse, redirect

class MiddleWare(MiddlewareMixin):
    def process_request(self, request):
        # print("request.path_info",request.path_info)
        if request.session.get("is_logined"):
            return
        else:
            # request.path_info 用户访问的url
            accetp_urls = [
                "/shuati_app/login/",          # 登录
                "/",                            # 首页
                "/shuati_app/getRandomQuestion/",
            ]

            if request.path_info in accetp_urls:
                return
            else:
                pattern = r'^static/.*'
                # 如果匹配失败，返回 NONE
                match = re.search(pattern, request.path)
                if not match:
                    return
                return redirect("/shuati_app/login/?message=你还没有登录，无权访问，请先登录")
            # return

    def process_response(self, request, response):
        return response
