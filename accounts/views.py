from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def login_view(request):
    if request.user.is_authenticated:
        return redirect('moments:home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('moments:home')
        else:
            messages.error(request, '用户名或密码错误')

    return render(request, 'accounts/login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('accounts:login')


@login_required
def profile_view(request):
    if request.method == 'POST':
        request.user.nickname = request.POST.get('nickname', '')
        request.user.bio = request.POST.get('bio', '')
        if 'avatar' in request.FILES:
            request.user.avatar = request.FILES['avatar']
        request.user.save()
        messages.success(request, '个人信息已更新')
        return redirect('accounts:profile')

    return render(request, 'accounts/profile.html')


@login_required
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not request.user.check_password(old_password):
            messages.error(request, '原密码错误')
        elif new_password != confirm_password:
            messages.error(request, '两次输入的密码不一致')
        elif len(new_password) < 4:
            messages.error(request, '密码至少4位')
        else:
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, '密码已修改')
            return redirect('accounts:profile')

    return render(request, 'accounts/change_password.html')
