from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from django.utils import timezone

from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView)

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login
from datetime import date

def About(request):
    return render(request,'about.html')

def Index(request):
    return render(request,'index.html')
def Contact(request):
    return render(request,'contact.html')
def user_login(request):
    error=""
    if request.method=='POST':
        u = request.POST.get('emailid')
        p = request.POST.get('pwd')
        user = authenticate(username=u,password=p)
        try:
            if user:
                login(request, user)
                error="no"
            else:
                error="yes"
        except:
            error="yes"
    d = {'error':error}
    return render(request,'login.html')
def login_admin(request):
    error=""
    if request.method=='POST':
        u = request.POST.get('uname')
        p = request.POST.get('pwd')
        user = authenticate(username=u,password=p)
        try:
            if user.is_staff:
                login(request, user)
                error="no"
            else:
                error="yes"
        except:
            error="yes"
    d = {'error':error}
    return render(request,'login_admin.html',d)

def signup(request):
    error=""
    if request.method=='POST':
        f = request.POST['firstnamey']
        l = request.POST['lastname']
        c = request.POST['contact']
        e = request.POST['emailid']
        p = request.POST['password']
        b = request.POST['branch']
        r = request.POST['role']
        try:
            user = User.objects.create_user(username=e,password=p,first_name=f,last_name=l)
            Signup.objects.create(User=user,contact=c,branch=b,role=r)
            error="no"
        except:
            error="yes"
    d={'error':error}
    return render(request,'signup.html',d)
def admin_home(request):

    return render(request,'admin_home.html')
def Logout(request):
    logout(request)
    return render('index')
def Profile(request):
    if not request.user.is_authenticated:
        return redirect('login')

    User = User.objects.get(id=request.User.id)
    data = Signup.objects.get(User = User)
    d = {'data':data,'user':user}
    return render(request,'profile.html',d)
def Edit_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    User = User.objects.get(id=request.User.id)
    data = Signup.objects.get(User = User)
    error = False
    if request.method == 'POST':
        f = request.POST['firstname']
        l = request.POST['lastname']
        c = request.POST['contact']
        b = request.POST['branch']
        User.first_name = f;
        User.last_name = l;
        data.contact = c;
        data.branch = b;
        User.save()
        data.save()
        error=True
    d = {'data':data,'user':User,'error':error}


    return render(request,'edit_profile.html',d)
def Changepwd(request):
    if not request.user.is_authenticated:
        return redirect('login')
    error = ""
    if request.method=="POST":
        o = request.POST['old']
        n = request.POST['new']
        c = request.POST['confirm']
        if c==n:
            u = User.objects.get(username__excat=request.user.username)
            u.set_password(n)
            u.save=()
            error="no"
        else:
            error="yes"
    '''User = User.objects.get(id=request.User.id)
    data = Signup.objects.get(User = User)'''
    d = {'error':error}
    return render(request,'changepwd.html',d)
def upload_notes(request):
    error=""
    if request.method=='POST':
        b = request.POST['branch']
        s = request.POST['subject']
        n = request.POST['notesfile']
        f = request.FILES['filetype']
        d = request.POST['description']
        u = User.objects.filter(username=request.User.username)

        try:
            Notes.objects.create(User=u,uploadingdate=date.today(),branch=b,subject=s,
            notesfile=n ,filetype=f,description=d,status='pending')
            error="no"
        except:
            error="yes"
    d={'error':error}
    return render(request,'upload_notes.html',d)

# Create your views here.
