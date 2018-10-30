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
from my_blog.settings import SECRET_KEY as SALT
from .forms import add_comment,outside_img,release_forms
from article.models import Article,Comment_db,IMG,Article_examine,User_data,Search_db

import datetime
import base64
import hashlib 
import random
import time
import json
import cgi
# import threading



def home(request):
    return render(request, 'home.html')

def get_home_articles(request,page):
    post_list = Article.objects.all()[page*5:(page+1)*5]
    archive_json = []
    for post in post_list:
        img_obtain=True
        text_temp=Article_mix(post.content)
        archive_json.append({'content':{'text':'','img':None},'title':cgi.escape(post.title),'id':post.id,'user':post.user,'date_time':post.date_time.strftime('%Y-%m-%d'),
            'examine_time':post.examine_time.strftime('%Y-%m-%d'),'comments_quantity':post.comments_quantity,'label':cgi.escape(post.label)})
        for text in text_temp:
            if len(archive_json[-1]['content']['text'])>150 and not img_obtain:
                break
            if img_obtain and text['type']=='img':
                archive_json[-1]['content']['img']=text['date_1']
                img_obtain=False
            elif img_obtain and text['type']=='code':
                archive_json[-1]['content']['code']=cgi.escape(text['date_1'])
                img_obtain=False
            else:
                pass
            if text['text']!=None and len(archive_json[-1]['content']['text'])<150:
                archive_json[-1]['content']['text']+=cgi.escape(text['text'])
        archive_json[-1]['content']['text']=archive_json[-1]['content']['text'][:150]
    return HttpResponse(json.dumps(archive_json))

def me(request):
    return render(request,'me.html',{'html_title':'关于我_'})

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
    post.label=post.label.split('#')
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
        'comment_content':comment_content,'User_name':User_name,'Result':Result,'html_title':post.title+'_'})

def archive(request):
    post_list = Article.objects.all()  
    return render(request,'archive.html',{'post_list' : post_list,'html_title':'列表_'})

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

    form_url = outside_img()
    return render(request, 'uploadimg.html',{'form_url' : form_url,'img_id' : new_img,'html_title':'上传图片_'})

def get_img(request,page):
    imgs_db = IMG.objects.all()[page*5:(page+1)*5]
    imgs_json = ({"len":len(imgs_db),"data":[]})
    for img in imgs_db:
        imgs_json["data"].append({"id":img.id,"url":img.url})
    return HttpResponse(json.dumps(imgs_json))

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
    return render(request, 'release.html',{'form' : form,'post_list':post_list,'html_title':'发布博客_'})

def examine(request):
    cookie_data = cookie_verification(request)
    if type(cookie_data) != dict:
        return HttpResponseRedirect('/exit/')
    if not cookie_data['admin']:
        return HttpResponseRedirect('/Error')
    examine_data = Article_examine.objects.filter(visible = True)
    return render(request, 'examine.html',{'post_list' : examine_data,'html_title':'审核博客_'})

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
        ,'permissions':cookie_data['admin'],'html_title':'个人中心_'})

def change_password(request):
    name = obtain_cookie_name(request)
    if name == None:
        return HttpResponse('{"state":2,"info":"Nome"}')
    if request.method == 'POST':
        old_password=request.POST.get('old_password','')
        password=request.POST.get('password','')
        cookie_data = loing_verification(name,old_password)
        if type(cookie_data) == str:
            return HttpResponse('{"state":1,"info":"'+cookie_data+'"}')
        elif User_format(name,password)==str:
            return HttpResponse('{"state":1,"info":"'+User_format(name,password)+'"}')
        else:
            User_db = User_data.objects.get(name=name)
            User_db.password = sha256_s(password+SALT)
            User_db.save()
            cookie_data = loing_verification(name,password)
            return HttpResponse('{"state":0,"info":"OK","cookie_name":"'+cookie_data['cookie_name']+'","cookie_password":"'+cookie_data['cookie_password']+'"}')
    return HttpResponse('{"state":1,"info":"Nome"}')

def login(request):
    if request.method == 'POST':
        name=request.POST.get('name','')
        password=request.POST.get('password','')
        cookie_data = loing_verification(name,password)
        if type(cookie_data) != str:
            return HttpResponse('{"state":0,"info":"OK","cookie_name":"'+cookie_data['cookie_name']+'","cookie_password":"'+cookie_data['cookie_password']+'"}')
        else:
            return HttpResponse('{"state":1,"info":"'+cookie_data+'"}')
    return HttpResponse('{"state":2,"info":"Nome"}')

def registered(request):
    if request.method == 'POST':
        name = request.POST.get('name','')
        password = request.POST.get('password','')
        cookie_data = registered_verification(name,password)
        if type(cookie_data) != str:
            return HttpResponse('{"state":0,"info":"OK","cookie_name":"'+cookie_data['cookie_name']+'","cookie_password":"'+cookie_data['cookie_password']+'"}')
        else:
            return HttpResponse('{"state":1,"info":"'+cookie_data+'"}')
    return HttpResponse('{"state":2,"info":"Nome"}')

def obtain_name(request):
    test=obtain_cookie_name(request)
    if(test):
        return HttpResponse('{"login":true,"name":"'+test+'"}')
    else:
        return HttpResponse('{"login":false}')

def port_search(request):
    if request.method == 'POST':
        keyword=request.POST.get('keyword','')
        article_list = Article.objects.all()
        temp_lost = []
        for article in article_list:
            weight = 0
            content_text = False
            weight += article.content.count(keyword)
            if weight:
                position = article.content.find(keyword)
                if position < 20:
                    content_text = article.content[:position+20]
                else:
                    content_text = article.content[position-20:position+20]
            if article.title.find(keyword)!=-1 or article.label.find(keyword)!=-1:
                weight+=10
                if content_text == False:
                    content_text = article.content[:20]
            if weight!=0:
                temp_lost.append({'id':article.id,"weight":weight,'content':{'text':cgi.escape(content_text)},'title':cgi.escape(article.title),
                    'user':article.user,'date_time':article.date_time.strftime('%Y-%m-%d'),'examine_time':article.examine_time.strftime('%Y-%m-%d'),
                    'comments_quantity':article.comments_quantity,'label':cgi.escape(article.label)})
        if(len(temp_lost)==0):
            return HttpResponse(json.dumps({"state":1,"info":"没有搜索结果","track":None,"end":True}))
        sort_list = []
        ranking = 0
        while True:
            ranking += 1
            if len(temp_lost)==1:
                sort_list.append(temp_lost[0])
                break
            position=0
            high_weight=0
            position=0
            for i in range(len(temp_lost)):
                if temp_lost[i]['weight'] > high_weight:
                    high_weight=temp_lost[i]['weight']
                    position=i
            sort_list.append(temp_lost[position])
            del temp_lost[position]
        if(len(sort_list)<=5):
            return HttpResponse(json.dumps({"state":0,"data":sort_list,"track":None,"end":True}))
        else:
            marking = sha256_s(random_s())[:16]
            Search_db.objects.create(marking = marking,page_quantity = len(sort_list)-5,page = json.dumps(sort_list[5:]))
            # arrangement_thread = threading.Thread(target = SearchArrangementThread)
            # arrangement_thread.start()
            return HttpResponse(json.dumps({"state":0,"data":sort_list[:5],"track":marking,"end":False}))
    return HttpResponse(json.dumps({"state":2,"end":True}))

def surplus_search(request):
    if request.method == 'GET':
        track = request.GET['track']
        end = request.GET['end']
        try:
            search = Search_db.objects.get(marking=track)
        except :
            if(end == 'true'):
                return HttpResponse('')
            else:
                return HttpResponse(json.dumps({"state":0,"info":"没有更多的结果","end":True}))
        if(end == 'true'):
            search.delete()
            return HttpResponse('')
        dumps_json = json.loads(search.page)
        if(int(search.page_quantity)<=5):
            search.delete()
            return HttpResponse(json.dumps({"state":0,"data":dumps_json,"end":True}))
        search.page_quantity-=5
        search.page=json.dumps(dumps_json[5:])
        search.save()                
        return HttpResponse(json.dumps({"state":0,"data":dumps_json,"end":True}))
    return HttpResponse(json.dumps({"state":3,"end":True}))

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

def registered_verification(name,password):
    result = User_format(name,password)
    if result != None:
        return result
    try:
        User_db = User_data.objects.get(name=name)
    except :
        pass
    else:
        return '用户名以存在'
    User_data.objects.create(name = name,password = sha256_s(password+SALT))
    return loing_verification(name,password)

def loing_verification(name,password):
    result = User_format(name,password)
    if result != None:
        return result
    try:
        User_db = User_data.objects.get(name=name)
    except :
        return '没有这个用户'
    if User_db.password != sha256_s(password+SALT):
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

def User_format(name,password):
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
            mix.append({'text':text,'type':None,'date_1':None,'date_2':None})
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
            rich=text[:text.find('@}')]
            rich_type=rich[:rich.find('|')]
            if rich_type == 'img':
                mix.append({'text':text_temp,'type':'img','date_1':img_id_url(rich[rich.find('|')+1:])})
            elif rich_type == 'a':
                rich=rich[rich.find('|')+1:]
                mix.append({'text':text_temp,'type':'a','date_1':rich[:rich.find('|')],'date_2':rich[rich.find('|')+1:]})
            elif rich_type == 'code':
                rich=rich[rich.find('|')+1:]
                mix.append({'text':text_temp,'type':'code','date_1':rich[rich.find('|')+1:]})
            else:
                mix.append({'text':text,'type':None,'date_1':None,'data_2':None})
            text=text[text.find('@}')+2:]

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

# def SearchArrangementThread():
#     try:
#         search = Search_db.objects.filter(examine_time__lte=datetime.date.today()-datetime.timedelta(days=2))
#     except :
#         pass 
#     else:
#         search.delete()