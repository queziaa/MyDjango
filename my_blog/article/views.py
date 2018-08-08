#coding=utf-8
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect  
from django.http import HttpResponse
from django.urls import reverse  
from datetime import datetime
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone  


from .forms import add_comment,outside_img,release_forms,registered_foms,cehange_password_foms
from article.models import Article,Comment_db,IMG,Article_examine,User_data

import datetime
import base64
import hashlib 
import random
import time
import json



def home(request):
    post_list = Article.objects.all()  
    for num in range(len(post_list)):
        text_temp=Article_mix(post_list[num].content)
        post_list[num].content={'text':'','img':None}
        for text in text_temp:
            if text['text']==None:
                continue
            post_list[num].content['text']=post_list[num].content['text']+text['text']
        post_list[num].content['img']=text_temp[0]['img']
    return render(request, 'home.html',{'post_list' : post_list})

def me(request):
    return render(request,'me.html')

def detailed(request,id):
    if request.method == 'POST':
        form = add_comment(request.POST)
        if form.is_valid():
            comment_content = form.cleaned_data['comment_content']
            ip=obtain_nameORip(request)
            comment_id = Comment_db.objects.create(comments_text = comment_content,
                ip_hash = ip)
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
        comment_content[-1].comments_text=Article_mix(comment_content[-1].comments_text)
        comment_ip_floor=comment_ip_floor-1
    cookie_data = cookie_verification(request)
    if type(cookie_data) == str:
        response = HttpResponseRedirect('/detailed/'+str(id)+'/')
        response.delete_cookie('password')
        response.delete_cookie('name')
        return response
    elif cookie_data == None:
        User_name = ip_base(request)
        Result = None
    else:
        User_name = cookie_data['name']
        Result = True
    Article_mix_content=Article_mix(post.content)
    return render(request, 'detailed.html',{'Article_mix_content':Article_mix_content,'post':post,'comment':comment,
        'comment_content':comment_content,'User_name':User_name,'Result':Result})

def archive(request):
    post_list = Article.objects.all()  
    return render(request,'archive.html',{'post_list' : post_list})


@csrf_exempt
def upload(request):
    new_img = None
    if request.method == 'POST':
        form = outside_img(request.POST)
        if form.is_valid():
            url = form.cleaned_data['img_url']
            new_img = img_db_repeat(url)
            if not new_img:
                new_img = IMG.objects.create(url = url ,img_type = False)
                new_img = str(new_img.id)
        else:
            myhash = hashlib.md5()
            img_temp = request.FILES.get('img')
            img_name = request.FILES.get('img').name
            img_name = img_name[img_name.rfind('.'):]
            while True:
                b = img_temp.read(8096)
                if not b :
                    break
                myhash.update(b)
            url = '/var/www/MyDjango/my_blog/static/img/'+myhash.hexdigest()+img_name
            new_img = img_db_repeat('/'+url)
            if not new_img:
                fobj = open(url,'wb');
                for chrunk in img_temp.chunks():
                    fobj.write(chrunk)
                fobj.close()
                new_img = IMG.objects.create(url = url[25:] ,img_type = True)
                new_img = str(new_img.id)

    imgs_db = IMG.objects.all()
    form_url = outside_img()
    return render(request, 'uploadimg.html',{'form_url' : form_url,'img_id' : new_img,'imgs':imgs_db})

def release(request):
    if request.method == 'POST':
        form = release_forms(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            label = form.cleaned_data['label']
            if not label:
                label = '!'
            else:
                temp_label =  ''
                if label[0] == '#':
                    label = label[1:]
                while False:
                    if label.find('#') != -1 and label.find('#')+1 < len(label):
                        temp_label = temp_label+'#'+label[:label.find('#')-1]
                        label = label[label.find('#')+1:]
                    else:
                        label = temp_label
                        break
            cookie_data = cookie_verification(request)
            if cookie_data == None:
                User_name = '#'+ip_base(request)
                Result = None
            else:
                User_name = '$'+cookie_data['name']
                Result = True
            Article_examine.objects.create(title = title,content = content,
                user = User_name,label = label)
            return HttpResponseRedirect('/release/')
        else:
            return HttpResponseRedirect('/404/')
    else:
        form = release_forms()

    post_list = Article_examine.objects.all() 
    return render(request, 'release.html',{'form' : form,'post_list':post_list})


def examine(request):
    cookie_data = cookie_verification(request)
    if type(cookie_data) != dict:
        return HttpResponseRedirect('/exit/')
    if not cookie_data['admin']:
        return HttpResponseRedirect('/Error')
    examine_data = Article_examine.objects.filter(visible = True)
    return render(request, 'examine.html',{'post_list' : examine_data})


def get_examine(request):
    cookie_data = cookie_verification(request)
    if type(cookie_data) != dict:
        return HttpResponseRedirect('/exit/')
    if not cookie_data['admin']:
        return HttpResponseRedirect('/Error')
    judge = request.GET.get('judge')
    if not judge.isdigit() or len(judge) > 10:
        return HttpResponseRedirect('/user/')
    article_db = Article_examine.objects.get(id = judge[1:])
    if judge[:1] == '1':
        Article.objects.create(title = article_db.title,content = article_db.content,
            examine_time = article_db.examine_time,user =article_db.user,label = article_db.label)
        article_db.delete()
    elif judge[:1] == '2':
        article_db.delete()
    elif judge[:1] == '3':
        article_db.visible = False
        article_db.save()
    else:
        return HttpResponseRedirect('/user/')
    return HttpResponseRedirect('/examine/')



def user(request):
    cookie_data = cookie_verification(request)
    if type(cookie_data) != dict:
        return HttpResponseRedirect('/exit/')
    return render(request,'user.html',{'name':cookie_data['name'],'id':cookie_data['id']
        ,'permissions':cookie_data['admin']})


def cehange_password(request):
    Result = None
    name = obtain_cookie_name(request)
    if name == None:
        return HttpResponseRedirect('/exit/')
    if request.method == 'POST':
        forms = cehange_password_foms(request.POST)
        if forms.is_valid():
            oid = forms.cleaned_data['oid']
            password = forms.cleaned_data['password']
            repeat_password = forms.cleaned_data['repeat_password']
            cookie_data = loing_verification(name,oid)
            if type(cookie_data) == str:
                Result = cookie_data
            elif password != repeat_password:
                Result = '两次密码不一致'
            elif User_format(name,password)==str:
                return User_format(name,password)
            else:
                User_db = User_data.objects.get(name=name)
                User_db.password = sha256_s(password+'e0058ff4746e011cb58ed32a19530baba71c3286612a0')
                User_db.save()
                cookie_data = loing_verification(name,password)
                cookie_url = HttpResponseRedirect('/')
                cookie_url.set_cookie("name",cookie_data['cookie_name'],1209600)
                cookie_url.set_cookie("password",cookie_data['cookie_password'],1209600)
                return cookie_url
        else:
            Result = '信息提交错误'
    forms = cehange_password_foms()
    cookie_datas = cookie_verification(request)
    return render(request,'cehange_password.html',{'name':cookie_datas['name'],'id':cookie_datas['id'],
        'permissions':cookie_datas['admin'],'forms':forms,'Result':Result})




def login(request):
    if request.method == 'POST':
        name=request.POST.get('name','')
        password=request.POST.get('password','')
        cookie_data = loing_verification(name,password)
        if type(cookie_data) != str:
            return HttpResponse('{"state": "0","info":"OK","cookie_name":"'+cookie_data['cookie_name']+'","cookie_password": "'+cookie_data['cookie_password']+'"}')
        else:
            return HttpResponse('{"state":"1","info":"'+cookie_data+'"}')
    return HttpResponse('{"state": "2","info":"Nome"}')

def registered(request):
    if request.method == 'POST':
        name = request.POST.get('name','')
        password = request.POST.get('password','')
        repeat_password = request.POST.get('repeat_password','')
        cookie_data = registered_verification(name,password,repeat_password)
        if type(cookie_data) != str:
            return HttpResponse('{"state": "0","info":"OK","cookie_name":"'+cookie_data['cookie_name']+'","cookie_password": "'+cookie_data['cookie_password']+'"}')
        else:
            return HttpResponse('{"state":"1","info":"'+cookie_data+'"}')
    return HttpResponse('{"state": "2","info":"Nome"}')

def obtain_name(request):
    test=obtain_cookie_name(request)
    if(test):
        return HttpResponse('{"login": "True","name": "'+ test +'"}')
    else:
        return HttpResponse('{"login": "False"}')
    




def exit(request):
    response = HttpResponseRedirect('/')
    response.delete_cookie('password')
    response.delete_cookie('name')
    return response

def e404(request):
    return render(request,'404.html')

def Error(request):
    return render(request,'Error.html')

#############################################################################
#############################################################################





def obtain_cookie_name(request):
    cookie_data = cookie_verification(request)
    if type(cookie_data) == dict:
        return cookie_data['name']
    else:
        return None

def obtain_nameORip(request):
    cookie_data = cookie_verification(request)
    if type(cookie_data) == dict:
        return '$'+cookie_data['name']
    else:
        return '#'+ip_base(request)


def registered_verification(name,password,repeat_password):
    result = User_format(name,password,repeat_password)
    if result != None:
        return result
    User_data.objects.create(name = name,password = sha256_s(password+'e0058ff4746e011cb58ed32a19530baba71c3286612a0'))
    return loing_verification(name,password)

def loing_verification(name,password):
    result = User_format(name,password)
    if result != None:
        return result
    try:
        User_db = User_data.objects.get(name=name)
    except :
        return '没有这个用户'
    if User_db.password != sha256_s(password+'e0058ff4746e011cb58ed32a19530baba71c3286612a0'):
        return '密码错误'
    cookie_name =  sha256_s(random_s())
    cookie_password = sha256_s(random_s())
    User_db.cookie_name = cookie_name
    User_db.cookie_password = sha256_s(cookie_password)
    User_db.cookie_time = datetime.datetime.now()+datetime.timedelta(weeks=3)
    User_db.save()
    return {'cookie_name':cookie_name,'cookie_password':cookie_password}

def cookie_verification(cookie):

    cookie_name = cookie.COOKIES.get('name')
    cookie_password = cookie.COOKIES.get('password')
    # print(cookie_name,cookie_password,cookie)
    if cookie_name == None or cookie_password == None:
        return None
    try:
        User_db = User_data.objects.get(cookie_name=cookie_name)
    except :
        return '登陆信息校验失败(N)'
    if User_db.cookie_password != sha256_s(cookie_password):
        return '登陆信息校验失败(P)'
    if User_db.cookie_time < timezone.now():
        return '登陆信息过期'
    return {'name':User_db.name,'id':User_db.id,'admin':User_db.admin}


def random_s():
    random.seed()
    time.sleep(random.random())
    random.seed()
    return str(random.random())

def sha256_s(value):
    sha256 = hashlib.sha256()
    sha256.update(value.encode('utf-8'))
    return sha256.hexdigest()

def User_format(name,password,repeat_password=None):
    if not name.isalnum():
        return '用户名只能用数字和字母'
    if len(name) > 14:
        return '用户名最多14位'
    if len(password) > 14:
        return '密码最多14位'
    if len(name) < 5:
        return '用户名最少5位'
    if len(password) < 5:
        return '密码最少5位'
    if repeat_password != None:
        try:
            User_db = User_data.objects.get(name=name)
        except :
            pass
        else:
            return '用户名以存在'
        if repeat_password != password:
            return '两次密码不一致'
    return None


def ip_base(request_ip):
    if 'HTTP_X_FORWARDED_FOR' in request_ip.META:  
        ip =  request_ip.META['HTTP_X_FORWARDED_FOR']  
    else:  
        ip = request_ip.META['REMOTE_ADDR']
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
        
def img_db_repeat(url_test):
    try:
        a=IMG.objects.get(url=url_test)
    except:
        return None
    else:
        return a.id

def Article_mix(text):
    mix=[]
    while True:
        if text.find('{@') == -1:
            mix.append({'text':text,'img':None})
            for temp in range(len(mix)):
                if mix[temp]['text']=='':
                    mix[temp]['text']=None
            return mix
        else:
            if text.find('@}') == -1:
                text=text[:text.find('{@')]+text[text.find('{@')+2:]
                continue
            text_temp=text[:text.find('{@')]
            text=text[text.find('{@')+2:]
            img=text[:text.find('@}')]
            img=img_id_url(img)
            text=text[text.find('@}')+2:]
            mix.append({'text':text_temp,'img':img})

def img_id_url(id):
    try:
        if not id.isdigit():
            return'/static/img/404.png'
    except:
        return'/static/img/404.png'

    try:
        a=IMG.objects.get(id=id)
    except:
        return '/static/img/404.png'
    else:
        return a.url
