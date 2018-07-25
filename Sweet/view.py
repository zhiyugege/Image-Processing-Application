from django.shortcuts import render
from django.http import HttpResponse
from . import img
from . import seam_carving
from . import dehanses
import json

def hello(request):
    context = {}
    context['hello'] = 'Hello World'
    return render(request,'hello.html',context)

def change(request):
    sat_value = request.POST.get('sat_value')
    br_value = request.POST.get('br_value')
    co_value = request.POST.get('co_value')
    path = img.change(int(br_value), int(sat_value), int(co_value))
    info = {'path':path}
    return HttpResponse(json.dumps(info), content_type="application/json")
    

def seam_change(request):

    width = request.POST.get('width')
    height = request.POST.get('height')
    ch_width = 512-int(width)
    ch_height = 384-int(height)
    SeamCarving = seam_carving.SeamCarving()
    path = SeamCarving.seamCarving(ch_width,ch_height)
    info = {'path':path}
    return HttpResponse(json.dumps(info), content_type="application/json")
    

def dehanse(request):

    path = dehanses.main()
    info = {'path':path}
    return HttpResponse(json.dumps(info), content_type="application/json")
# @accept_websocket
# def echo(request):
#     if not request.is_websocket():#判断是不是websocket连接
#         try:#如果是普通的http方法
#             message = request.GET['message']
#             return HttpResponse(message)
#         except:
#             return render(request,'hello.html')
#     else:
#         for message in request.websocket:
#             docter.start(request)

