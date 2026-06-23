import re
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile 

# 1. 회원가입 처리
def signup_view(request):
    if request.method == 'GET' and request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        nickname = request.POST.get('nickname')
        profile_character = request.POST.get('profile_character', 'basic')
        background_color = request.POST.get('profile_color', 'bg-red')

        # 입력 데이터 유지용 context
        context = {
            'username': username,
            'nickname': nickname,
            'profile_character': profile_character,
            'background_color': background_color
        }

        # 1. 아이디 중복 검사
        if User.objects.filter(username=username).exists():
            messages.error(request, "이미 존재하는 아이디입니다.")
            return render(request, 'accounts/signup.html', context)
        
        # 2. 닉네임 검사: 길이 (2자 이상 15자 이하)
        if not (2 <= len(nickname) <= 15):
            messages.error(request, "닉네임은 2자 이상 15자 이하로 설정해야 합니다.")
            return render(request, 'accounts/signup.html', context)
        
        # 3. 닉네임 검사: 특수문자 금지 (영문, 숫자, 한글만 허용)
        if not re.match(r'^[a-zA-Z0-9가-힣]+$', nickname):
            messages.error(request, "닉네임에 특수문자는 사용할 수 없습니다.")
            return render(request, 'accounts/signup.html', context)
        
        # (참고) 비밀번호 조건은 프로젝트 보안 정책에 맞게 자유롭게 유지하거나 수정하면 돼!
        
        user = User.objects.create_user(username=username, password=password)

        UserProfile.objects.create(
            user=user,
            nickname=nickname,
            profile_character=profile_character,
            background_color=background_color
        )

        messages.success(request, "회원가입이 완료되었습니다! 로그인을 진행해 주세요.")
        return redirect('login') 
    
    return render(request, 'accounts/signup.html')


# 2. 로그인 처리
def login_view(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
    
            try:
                nickname = user.userprofile.nickname
            except UserProfile.DoesNotExist:
                new_profile = UserProfile.objects.create(
                    user=user,
                    nickname=user.username,
                    profile_character='default_frog',
                    background_color='#FFFFFF'
                )
                nickname = new_profile.nickname

            messages.success(request, f"{nickname}님 환영합니다!")
            return redirect('home')
        else:
            messages.error(request, "올바른 아이디 혹은 비밀번호를 입력하세요.")
            return render(request, 'accounts/login.html')
        
    return render(request, 'accounts/login.html')

# 3. 로그아웃 처리
def logout_view(request):
    auth_logout(request)
    return redirect('login')