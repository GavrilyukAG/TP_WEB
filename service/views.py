# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.urls import reverse
from models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from forms import *
import logging

from django.views.decorators.csrf import csrf_exempt  # Ne ispolzovat
from django.http import JsonResponse
import json

logging.basicConfig()
logger = logging.getLogger(__name__)

# Create your views here.


def paginate(data, request):
    page = request.GET.get('page')
    paginator = Paginator(data, 3)
    try:
        return paginator.page(page)
    except PageNotAnInteger:
        return paginator.page(1)
    except EmptyPage:
        return paginator.page(paginator.num_pages)


def new(request):
    title = 'AskGA'
    header = 'New'
    items = paginate(Question.objects.newest(), request)
    return render(request, 'index.html', locals())


def hot(request):
    title = 'AskGA'
    header = 'Hot'
    items = paginate(Question.objects.hottest(), request)
    return render(request, 'index.html', locals())


def tag(request, tag_id):
    title = 'Tags'
    items = paginate(Question.objects.newest().filter(tags=tag_id), request)
    tag = Tag.objects.get(id=tag_id)
    return render(request, 'tag.html', locals())


def question(request, question_id):
    title = 'Question'
    question = Question.objects.get(id=question_id)
    items = paginate(Answer.objects.all().filter(question=question_id), request)
    form = AnswerForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            answer = Answer.objects(
                author=request.user.id,
                question=request.question.id,
                text=request.POST.get('text')
            )
    return render(request, 'question.html', locals())


def login(request):
    form = LoginForm()
    valid = True
    if request.POST:
        user = auth.authenticate(
            username=request.POST.get('username'),
            password=request.POST.get('password'),
        )
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            valid = False
            # errors = form.errors
    return render(request, 'login.html', locals())


def logout(request):
    auth.logout(request)
    return redirect(reverse('index'))


def register(request):
    form = RegisterForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            user = User.objects.create(
                username=request.POST.get('username'), # form.cleaned_data[]
                first_name=request.POST.get('first_name'),
                email=request.POST.get('email'),
                password=request.POST.get('password')
            )
            profile = Profile.objects(
                user=user,
                avatar=request.FILES.get('avatar')
            )
            profile.save()
            return redirect('/')
        else:
            valid = False
    return render(request, 'registration.html', locals())


@login_required(login_url='login')
def ask(request):
    form = AskForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            profile = request.user.profile
            question = Question.objects.create(
                author=profile,
                title=form.cleaned_data.get('title'),
                text=form.cleaned_data.get('text'),
            )
            tags = request.POST.get('tags').split(',')
            for item in tags:
                try:
                    tag = Tag.objects.get(title=item)
                    question.tags.add(tag)
                except:
                    tag = Tag(title=item)
                    tag.save()
                    question.tags.add(tag)

            return redirect('/') # rediret to question page
    return render(request, 'ask.html', locals())


@login_required(login_url='login')
def settings(request):
    form = SettingsForm(request.POST or None)
    if request.POST:
        user = User.objects.get(id=request.user.id)
        user = User.objects(
            username=form.cleaned_data.get('username'),
            email=form.cleaned_data.get('email'),
            password=form.cleaned_data.get('password'),
            first_name=form.cleaned_data.get('first_name'),
        )
        user.save()
        profile = Profile.objects.get(id=user)
        profile = Profile(
            avatar=form.cleaned_data('avatar')
        )
        profile.save()
        return redirect('/')
    return render(request, 'settings.html', locals())


@login_required
def profile(request):
    profile = request.user.profile
    if request.POST:
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile.avatar = form.cleaned_data['avatar']
            profile.save()
    return render(request, 'profile.html', locals())


@csrf_exempt # dont use
def vote(request):
    if request.POST:
        return JsonResponse(data=dict(status='ok'))
    else:
        return JsonResponse(data=dict(error='wrong request'))
