from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Profile, Post, Comment


# Home Page
def home(request):

    posts = Post.objects.all().order_by('-created_at')

    return render(
        request,
        'social/home.html',
        {'posts': posts}
    )


# Register
def register(request):

    if request.method == 'POST':

        form = UserCreationForm(request.POST)

        if form.is_valid():

            user = form.save()

            Profile.objects.create(user=user)

            login(request, user)

            return redirect('home')

    else:

        form = UserCreationForm()

    return render(
        request,
        'social/register.html',
        {'form': form}
    )


# Profile
def profile(request, username):

    profile_user = get_object_or_404(
        User,
        username=username
    )

    profile = get_object_or_404(
        Profile,
        user=profile_user
    )

    posts = Post.objects.filter(
        user=profile_user
    ).order_by('-created_at')
    followers = profile.followers.all()
    following = User.objects.filter(profile__followers=profile_user)

    is_following = False

    if request.user.is_authenticated:

        is_following = profile.followers.filter(id=request.user.id).exists()
        
        

    return render(
        request,
        'social/profile.html',
        {
            'profile_user': profile_user,
            'profile': profile,
            'posts': posts,
            'followers': followers,
            'following': following,
            'is_following': is_following,
            
        }
    )


# Create Post
@login_required
def create_post(request):

    if request.method == 'POST':

        content = request.POST.get('content')

        if content:

            Post.objects.create(
                user=request.user,
                content=content
            )

    return redirect('home')


# Like / Unlike
@login_required
def like_post(request, post_id):

    post = get_object_or_404(
        Post,
        id=post_id
    )

    if request.user in post.likes.all():

        post.likes.remove(request.user)

    else:

        post.likes.add(request.user)

    return redirect('home')


# Add Comment
@login_required
def add_comment(request, post_id):

    post = get_object_or_404(
        Post,
        id=post_id
    )

    if request.method == 'POST':

        content = request.POST.get('content')

        if content:

            Comment.objects.create(
                post=post,
                user=request.user,
                content=content
            )

    return redirect('home')


# Follow / Unfollow
@login_required
def follow_user(request, username):

    user_to_follow = get_object_or_404(
        User,
        username=username
    )

    profile = get_object_or_404(
        Profile,
        user=user_to_follow
    )

    if request.user == user_to_follow:
        return redirect(
            'profile',
            username=username
        )

    if request.user in profile.followers.all():

        profile.followers.remove(
            request.user
        )

    else:

        profile.followers.add(
            request.user
        )

    return redirect(
        'profile',
        username=username
    )
