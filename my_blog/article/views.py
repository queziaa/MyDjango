#coding=utf-8
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect  
from django.http import HttpResponse
from django.urls import reverse  
from article.models import Article
from article.models import Comment_db
from article.models import IMG
from datetime import datetime
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
import base64
import hashlib


from .forms import add_forms
from .forms import add_comment


# Create your views here.
def home(request):
    post_list = Article.objects.all()  #获取全部的Article对象
    return render(request, 'home.html',{'post_list' : post_list})

def me(request):
    return render(request,'me.html')

def detailed(request,id):
    if request.method == 'POST':
        form = add_comment(request.POST)
        if form.is_valid():
            comment_content = form.cleaned_data['comment_content']
            if 'HTTP_X_FORWARDED_FOR' in request.META:  
                ip =  request.META['HTTP_X_FORWARDED_FOR']  
            else:  
                ip = request.META['REMOTE_ADDR']
            ip=ip_base(ip)
            comment_id = Comment_db.objects.create(comments_text = comment_content,ip_hash = ip)
            post = Article.objects.get(id=id)
            post.comment_ip = (baseN(comment_id.id,32)+'@'+post.comment_ip)
            post.comments_quantity=post.comments_quantity+1
            post.save()
            return HttpResponseRedirect('/detailed/'+str(id)+'/')

    post = Article.objects.get(id=id)
    comment=add_comment()
    gather=comment_ip_decode(post.comment_ip)
    comment_ip_floor = post.comment_ip.count('@')
    comment_content=[]
    for test in gather:
        comment_content.append(Comment_db.objects.get(id=test))
        comment_content[-1].floor=comment_ip_floor
        comment_ip_floor=comment_ip_floor-1
    return render(request, 'detailed.html',{'post':post,'comment':comment,'comment_content':comment_content})

def archive(request):
    post_list = Article.objects.all()  
    return render(request,'archive.html',{'post_list' : post_list})


def test(request):
    if request.method == 'POST':# 当提交表单时
     
        form = add_forms(request.POST) # form 包含提交的数据
         
        if form.is_valid():# 如果提交的数据合法
            a = form.cleaned_data['a']
            b = form.cleaned_data['b']
            return HttpResponse(str(int(a) + int(b)))
     
    else:# 当正常访问时
        form = add_forms()
    return render(request, 'test.html', {'form': form})


def add(request):
    a = request.GET['a']
    b = request.GET['b']
    a = int(a)
    b = int(b)
    return HttpResponse(str(a+b))



def e404(request):
    return render(request,'404.html')


@csrf_exempt
def uploadImg(request):
    if request.method == 'POST':
        new_img = IMG(
            img=request.FILES.get('img'),
            name = request.FILES.get('img').name
        )
        new_img.save()
    return render(request, 'uploadimg.html')

@csrf_exempt
def showImg(request):
    imgs = IMG.objects.all()
    content = {
        'imgs':imgs,
    }
    for i in imgs:
        print (i.img.url)
    return render(request, 'showimg.html', content)

# def detail(request, id):
#     try:
#         post = Article.objects.get(id=str(id))
#     except Article.DoesNotExist:
#         raise Http404
#     return render(request, 'post.html', {'post' : post})

# def archives(request) :
#     try:
#         post_list = Article.objects.all()
#     except Article.DoesNotExist :
#         raise Http404
#     return render(request, 'archives.html', {'post_list' : post_list, 'error' : False})

# def about_me(request) :
#     return render(request, 'aboutme.html')

def ip_base(ip):
    print(ip)
    ip1=ip[:ip.find('.')]
    ip=ip[ip.find('.')+1:]
    ip2=ip[:ip.find('.')]
    ip=ip[ip.find('.')+1:]
    ip3=ip[:ip.find('.')]
    ip=ip[ip.find('.')+1:]
    ip=ip1.zfill(3)+'.'+ip2.zfill(3)+'.'+ip3.zfill(3)+'.'+ip.zfill(3)
    ip=ip+'ODhiYzgwNDIwZDNhY'
    a = hashlib.sha1()
    a.update(ip.encode('utf-8'))
    return str(base64.b64encode(a.hexdigest().encode('utf-8')))[2:12]


def baseN(num, b):
    return ((num == 0) and "0") or \
           (baseN(num // b, b).lstrip("0") + "0123456789abcdefghijklmnopqrstuvwxyz"[num % b])

def comment_ip_decode(ip_src):
    gather=[]
    while True:
        #if not (ip_src.count('@') and len(gather)<20):
        if not ip_src.count('@'):
            return gather
        test = ip_src[:ip_src.find('@')]
        ip_src=ip_src[ip_src.find('@')+1:]
        gather.append(int(test,32))