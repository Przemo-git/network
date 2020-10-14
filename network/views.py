# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from network.models import Post, Like, Following, User


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    if request.method == 'POST':
        content = request.POST['content']
        user = request.user
        data = Post(user=user, content=content)
        data.save()
        return HttpResponseRedirect(reverse('index'))

    result = Post.objects.all()
    ids = [p.id for p in result]
    content = [p.content for p in result]
    user = [p.user for p in result]
    time = [p.time for p in result]
    likes = [0]*len(ids)
    for i in range(len(ids)):
        likeCount = Like.objects.filter(post_id=ids[i])
        likes[i] = len(likeCount)
    posts = []
    for i in reversed(range(len(content))):
        posts.append({'id': ids[i] ,'content': content[i], 'user': user[i], 'time': time[i], 'likes': likes[i]})
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    print('paginator', paginator, page)
    return  render(request, 'network/index.html', {
        'posts': posts
    })


def profile(request, username):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    follow = Following.objects.filter(user=username)
    followed_by = Following.objects.filter(following=username)
    result = Post.objects.filter(user=username)
    print(username)
    ids = [p.id for p in result]
    content = [p.content for p in result]
    user = [p.user for p in result]
    time = [p.time for p in result]
    likes = [0] * len(ids)
    for i in range(len(ids)):
        likeCount = Like.objects.filter(post_id=ids[i])
        likes[i] = len(likeCount)
    posts = []
    for i in reversed(range(len(content))):
        posts.append({'id': ids[i], 'content': content[i], 'user': user[i], 'time': time[i], 'likes': likes[i]})
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    print('paginator', paginator, page)
    return render(request, 'network/profile.html', {
        'posts': posts,
        'follow': len(follow),
        'followed_by': len(followed_by),
        'user': username
    })


def login_view(request):
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'network/login.html', {
                'message': 'Invalid username and/or password.'
            })
    else:
        return render(request, 'network/login.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def likes(request, ID, user):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    check = Like.objects.filter(post_id=ID, user=user)
    if len(check)<1:
        obj = Like(post_id=ID, user=user)
        obj.save()
    else:
        check.delete()
    result = Like.objects.filter(post_id=ID)
    return HttpResponse(len(result))

def follow_user(request, currentuser, user):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    check = Following.objects.filter(user=currentuser, following=user)
    if len(check)<1:
        obj = Following(user=currentuser, following=user)
        obj.save()
    else:
        check.delete()
    result = Following.objects.filter(following=user)
    return HttpResponse(len(result))

def unfollow_user(request, user, currentuser):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("login"))
        check = Following.objects.filter(user = currentuser, following = user)
        if len(check) == 1:
            check.delete()
        result = Following.objects.filter(following = user)
        return HttpResponse(len(result))

def following_page(request, user):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    check = Following.objects.filter(user =  user)
    usernames = [p.following for p in check]
    result = Post.objects.filter(user__in = usernames)
    print(usernames)
    ids = [p.id for p in result]
    content = [p.content for p in result]
    user = [p.user for p in result]
    time = [p.time for p in result]
    likes =[0]*len(ids)
    for i in range(len(ids)):
        likeCount = Like.objects.filter(post_id=ids[i])
        likes[i] = len(likeCount)
    posts = []
    followed_by = Following.objects.filter(following = user)
    for i in reversed(range(len(content))):
        posts.append({'id' : ids[i],'user' : user[i], 'content' : content[i], 'time' : time[i], 'likes': likes[i]})
    paginator = Paginator(posts,10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, "network/following_page.html" ,{
        'posts' : posts,
        'follow' : len(check),
        'followed_by' : len(followed_by)
    })

def edit_page(request, post_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    result = Post.objects.filter(pk=post_id, user=request.user)
    if len(result)<1:
        return render(request, 'network/error.html', {
            'message': 'Post request error'
        })
    ids =[p.id for p in result]
    content = [p.content for p in result]
    return render(request, 'network/edit.html', {
        'id': ids[0],
        'content': content[0]
    })

def updated(request, post_id, content):
    result = Post.objects.filter(pk = post_id, user=request.user).update(content=content)
    return HttpResponse('Post update, go to the All Posts page to see the changes')