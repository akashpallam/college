from ast import Return
from multiprocessing import context
from operator import imod
from email import message
from email.mime import image
from .models import *
import os
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect

# Create your views here.
def home(request):
    return render(request,'home.html')

def register(request):
    return render(request,'signup.html')


def sign_up(request):
    if request.method =='POST':
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        address=request.POST.get('address')
        email=request.POST.get('email')
        urname=request.POST.get('uname')
        passw=request.POST.get('passw')
        cpassw=request.POST.get('cpassw')
        gender=request.POST.get('gender')
        mobile=request.POST.get('mobile')
        if request.FILES.get('file') is not None:
            image=request.FILES['file']
        else:
            image="/static/image/user.png"
        if cpassw==passw:
            if User.objects.filter(username=urname).exists():
                messages.info(request,'this user name is already exits')
                return redirect('sign_up')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'this email is already exists')
                return redirect('sign_up')
            else:
                user=User.objects.create_user(first_name=fname,last_name=lname,email=email,username=urname,password=passw)
                user.save()
                u=User.objects.get(id=user.id)
                member=UserMember(user_address=address,user_gender=gender,user_mobile=mobile,user=u,user_photo=image)
                member.save()
                return redirect('load_loginpage')
    return redirect('register')

def load_loginpage(request):
    return render(request,'login.html')

def userlogin(request):
    if request.method == 'POST':
        try:
            username=request.POST['uname']
            password=request.POST['password']
            user=auth.authenticate(username=username,password=password)
            request.session['uid']=user.id
            if user is not None:
                if user.is_staff:
                    login(request,user)
                    return redirect('welcomeadmin')
                else:
                    login(request,user)
                    auth.login(request,user)
                    return redirect('load_welcome_page')
            else:
                messages.info(request,'invalid usename or password, Try again')
                return redirect('userlogin')
        except:
            messages.info(request,'invalid username or password, Try again later')
            return redirect('login.html')
    else:
        return render(request,'login.html')

@login_required(login_url='load_loginpage')
def welcomeadmin(request):
    return render(request,'adhome.html')

@login_required(login_url='load_loginpage')
def load_admin_home(request):
    teachers=UserMember.objects.all()
    return render(request,'admin.html',{'teachers':teachers})

@login_required(login_url='load_loginpage')
def load_welcome_page(request):
    return render(request,'welcome.html')

@login_required(login_url='load_loginpage')
def admin_details(request):
    teachers=UserMember.objects.all()
    return render(request,'admindetails.html',{'teachers':teachers})

def logout(request):
    request.session["uid"]=""
    auth.logout(request)
    return redirect('load_loginpage')



@login_required(login_url='load_loginpage')
def add_course(request):
    if request.method=='POST':
        cors=request.POST['course']
        cfee=request.POST['cfee']
        print(cors)
        crs=course()
        crs.course_name=cors
        crs.fee=cfee
        crs.save()
        print("hlo")
        return redirect('student1')
    return render(request,'course.html')
    
@login_required(login_url='load_loginpage')
def course1(request):
    uid=User.objects.get(id=request.session["uid"])
    return render(request,'course.html',{'uid':uid})

@login_required(login_url='load_loginpage')
def student1(request):
    courses=course.objects.all()
    context={'courses':courses}
    return render(request,'student.html',context)

@login_required(login_url='load_loginpage')
def show_student_details(request):
    std=student.objects.all()
    return render(request,'stdtable.html',{'std':std})

@login_required(login_url='load_loginpage')
def show_student_details2(request):
    std=student.objects.all()
    return render(request,'stdtable2.html',{'std':std})

@login_required(login_url='load_loginpage')
def add_student(request):
    if request.method=='POST':
        sname=request.POST['sname']
        address=request.POST['address']
        age=request.POST['age']
        jdate=request.POST['jdate']
        sel1=request.POST['sel']
        
        course1=course.objects.get(id=sel1)
        std=student(std_name=sname,std_address=address,std_age=age,std_date=jdate,course=course1)
    std.save()
    print("hlo")
    return redirect('show_student_details')

@login_required(login_url='load_loginpage')
def profile(request):
    user=UserMember.objects.filter(user=request.user)
    context={'user': user}
    return render(request,'profile.html', context)

@login_required(login_url='load_loginpage')
def edit_tutor(request):
    user= UserMember.objects.filter(user=request.user)
    context={'user': user}
    return render(request,'tredit.html', context)

def update_tutor(request):
    if request.method=='POST':
        print("hello")
        tutor=UserMember.objects.get(user=request.user)
        tutor.user.first_name=request.POST.get('fname')
        tutor.user.last_name=request.POST.get('lname')
        tutor.user.username=request.POST.get('uname')
        tutor.user.email=request.POST.get('email')
        tutor.user_address=request.POST.get('address')
        tutor.user_gender=request.POST.get('gender')
        tutor.user_mobile=request.POST.get('mobile')
        if request.FILES.get('file') is not None:
            if not tutor.user_photo=="/statit/image/user.png":
                tutor.user_photo=request.FILES['file']
            else:
                tutor.user_photo=request.FILES['file']
        else:
            tutor.user_photo=="/statit/image/user.png"
        tutor.user.save()
        print("hello")
        tutor.save()
        print("hellohello")
        return redirect('profile')
    user=UserMember.objects.get(user=request.user)
    context={'user': user}
    print("trapped")
    return render(request,'profile.html',context)

@login_required(login_url='load_loginpage')
def edit_student(request,pk):
    students=student.objects.get(id=pk)
    courses=course.objects.all()
    return render(request,'stedit.html',{'students':students,'cou':courses})

@login_required(login_url='load_loginpage')
def update_student(request,pk):
    if request.method=='POST':
        student1 =student.objects.get(id=pk)
        
        student1.std_name = request.POST.get('sname')
        student1.std_address = request.POST.get('address')
        student1.std_age = request.POST.get('age')
        student1.std_date = request.POST.get('jdate')
       
        cid=request.POST.get('cname')
        cor=course.objects.get(id=cid)
        student1.course=cor

        
        student1.save()
        return redirect('show_student_details')
    return render(request, 'stedit.html')


@login_required(login_url='load_loginpage')
def delete_tutor(request,pk):
    user=UserMember.objects.filter(id=pk)
    user.delete()
    return redirect('load_admin_home')


@login_required(login_url='load_loginpage')
def delete_std(request,pk):
    std=student.objects.filter(id=pk)
    std.delete()
    return redirect('show_student_details')














