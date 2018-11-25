from django.shortcuts import render
from django.http import HttpResponse
from django_hosts.resolvers import reverse
from django.http import HttpResponseRedirect  

def home(request,page=False):
    hosts = request.get_host().split('.')
    if hosts[-3] == 'blog':
        hosts[-3] = 'www'
        return HttpResponseRedirect('https://'+'.'.join(hosts))
    elif hosts[-3] == 'cv':
        hosts[-3] = 'r'
        return HttpResponseRedirect('https://'+'.'.join(hosts))
    else:
        return render(request,'www_home.html')