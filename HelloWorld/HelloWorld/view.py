from django.http import HttpResponse
from django.shortcuts import render
from TestModel.models import Test
import json


def hello(request):
    context = {}
    context["hello"] = "hello world2"
    return render(request, "temp_hello.html", context)
    # return HttpResponse("hello world")


def addUser(request):
    ret = {}
    ret["desc"] = "success"
    name = request.GET.get("name")
    if  not name:
        ret["desc"] = "没有传入用户名"
        return HttpResponse(json.dumps(ret))

    pwd = request.GET.get("pwd")
    if  not name:
        ret["desc"] = "没有传入密码"
        return HttpResponse(json.dumps(ret))


    #检查是否重复

    obj = Test.objects.filter(name=name,pwd=pwd)
    if obj:
        ret["desc"] = "用户名和密码已存在"
        return HttpResponse(json.dumps(ret))

    t1 = Test(name=name, pwd=pwd)
    t1.save()
    ret["desc"] = "success"
    ret["name"] = name
    ret["pwd"] = pwd
    return HttpResponse(json.dumps(ret))
