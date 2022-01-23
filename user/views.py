from django.shortcuts import render

# Create your views here.

from django.shortcuts import render,redirect
from .models import UserModel
from django.http import HttpResponse
from django.contrib.auth import get_user_model #사용자가 데이터베이스 안에 있는지 확인하는 함수
from django.contrib import auth
from django.contrib.auth.decorators import login_required

# Create your views here.
def sign_up_view(request):
    if request.method =='GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request,'user/sign-up.html')


        # render(render)해서 오류났었음, request  제대로 적었는지 확인
        return render(request,'user/sign-up.html')
    elif request.method == 'POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        password2 = request.POST.get('password2','')
        bio = request.POST.get('bio','')


        if password != password2:
            return render(request,'user/sign-up.html', {'error':'패스워드를 확인해주세요'})
        else:
            if username == '' or password == '':
                return render(request, 'user/sign-up.html', {'error':'사용자이름과 패스워드는 필수값입니다.'})
            exist_user = get_user_model().objects.filter(username=username)
            if exist_user:
                return render(request,'user/sign-up.html', {'error':'사용자가 존재합니다'})
            else:
                UserModel.objects.create_user(username=username,password=password,bio=bio)
                return redirect('/sign-in')


def sign_in_view(request):
    if request.method == 'POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')

        # 중복확인이 구현안된 상태에서 같은아이디를 두개 만들고 로그인하면 두개의 값이 전달되면서 오류발생
        me = auth.authenticate(request, username=username,password=password)
        if me is not None:
            auth.login(request, me)
            return redirect('/')
        else:
            return render(request,'user/sign-in.html',{'error':'아이디와 패스워드를 확인해주세요'})

    elif request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request,'user/sign-in.html')

@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')

# user/views.py

@login_required
def user_view(request):
    if request.method == 'GET':
        # 사용자를 불러오기, exclude와 request.user.username 를 사용해서 '로그인 한 사용자'를 제외하기
        user_list = UserModel.objects.all().exclude(username=request.user.username)
        return render(request, 'user/user_list.html', {'user_list': user_list})


@login_required
def user_follow(request, id):
    me = request.user
    click_user = UserModel.objects.get(id=id)
    if me in click_user.followee.all():
        click_user.followee.remove(request.user)
    else:
        click_user.followee.add(request.user)
    return redirect('/user')

