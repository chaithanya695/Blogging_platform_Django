from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import Profile
from blog.models import Post
from .forms import ProfileForm
from django.contrib.auth.decorators import login_required



def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            messages.success(request, "Account created successfully!")
            return redirect('accounts:login')

        else:
            messages.error(request, "Please fix the errors below")

    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


def user_login(request):
    error = None

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('blog:post_list')
        else:
            error = "Invalid username or password"

    return render(request, 'login.html', {'error': error})


def user_logout(request):
    logout(request)
    return redirect('blog:post_list')

def profile_view(request, username):
    user_obj = get_object_or_404(User, username=username)

    profile, created = Profile.objects.get_or_create(user=user_obj)

    posts = Post.objects.filter(author=user_obj)

    return render(request, 'profile.html', {
        'profile': profile,
        'user_obj': user_obj,
        'posts': posts
    })

@login_required
def edit_profile(request):

    profile = request.user.profile

    if request.method == "POST":

        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():
            form.save()

            return redirect(
                'accounts:profile',
                username=request.user.username
            )

    else:

        form = ProfileForm(
            instance=profile
        )

    return render(
        request,
        'edit_profile.html',
        {'form': form}
    )