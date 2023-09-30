from django.http import HttpResponse


# Create your views here.
def index(request):
    text = '<h1 style="text-align: center;margin-top: 20%;"> <a href="/shuati_app">点击进入答题系统</a></h1>'
    return HttpResponse(text)
