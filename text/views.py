# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from text.models import Text, UserProfile, Comment, Like
from django.http import Http404, HttpResponse, JsonResponse
from django.db.models import Avg, Max, Min, Count
from django.contrib.auth import authenticate, login, logout
from text.forms import UserLoginForm, UserRegistrationForm, WriteTextForm, WriteCommentForm
from django.contrib.contenttypes.models import ContentType
import json
import datetime

def text_list(request):
    texts = Text.objects.all()[:20]
    texts = texts.select_related('author')
    # texts = texts.annotate(Count('comment'))

    # model_type = ContentType.objects.get_for_model(Text)
    # a = Like.objects.filter(content_type=model_type, object_id__in = list(texts.values_list('id', flat=True)))
    # b = a.values('object_id').annotate(Count('object_id'))
    # likes = {elem['object_id'] : elem['object_id__count'] for elem in b}
    for text in texts:
        text.comment__count = text.comment_set.count()
        text.likes__count = text.likes.count()
        # if (likes.has_key(text.id)):
        #     text.likes__count = likes[text.id]
        text.author__like = len(text.likes.filter(author=request.user.id))

    return render(
        request, 'text/text_list.html', 
        {'texts': texts}
    )


def text_detail(request, text_id):
    try:
        text = Text.objects.select_related('author').get(id=text_id)
        text.views += 1
        text.save()

        text.likes__count = text.likes.all().count()
        text.author__like = len(text.likes.filter(author=request.user.id))

        comments = text.comment_set.all()
        comments = comments.select_related('author')
        text.comment__count = comments.count()

        model_type = ContentType.objects.get_for_model(Comment)
        a = Like.objects.filter(content_type=model_type, object_id__in = list(comments.values_list('id', flat=True)))
        b = a.values('object_id').annotate(Count('object_id'))
        likes = {elem['object_id'] : elem['object_id__count'] for elem in b}
        for comment in comments:
            comment.likes__count = 0
            if (likes.has_key(comment.id)):
                comment.likes__count = likes[comment.id]
            comment.author__like = len(comment.likes.filter(author=request.user.id))

    except Text.DoesNotExist:
        raise Http404

    # if request.user.is_authenticated:
        # if not request.method == 'POST':
    form = WriteCommentForm()

    return render(
        request, 'text/text_detail.html',
        {'text': text, 'comments': comments, 'form':form}
    )


def text_author(request, author_id):
    try:
        author = UserProfile.objects.get(id=author_id)
        texts = author.text_set.annotate(Count('comment'))[:20]

        model_type = ContentType.objects.get_for_model(Text)
        a = Like.objects.filter(content_type=model_type, object_id__in = list(texts.values_list('id', flat=True)))
        b = a.values('object_id').annotate(Count('object_id'))
        likes = {elem['object_id'] : elem['object_id__count'] for elem in b}
        for text in texts:
            text.likes__count = 0
            if (likes.has_key(text.id)):
                text.likes__count = likes[text.id]
            text.author__like = len(text.likes.filter(author=request.user.id))

    except UserProfile.DoesNotExist:
        raise Http404    
    return render(
        request, 'text/text_author.html',
        {'author': author, 'texts': texts}
    )


def logout_author(request):
    logout(request)
    return redirect('text:text_list')


def login_form(request, state):
    return render(
        request, 'text/author_login.html', 
        {'state': state}
    )


def login_author(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('text:text_list')
            else:
                return render(request, 'text/author_login.html', {'form': form})
    else:   
        form = UserLoginForm()

    return render(request, 'text/author_login.html', {'form': form})


def registr_author(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            return redirect('text:text_list')
    else:   
        form = UserRegistrationForm()

    return render(request, 'text/author_registr.html', {'form': form})


def write_text(request):
    if request.method == 'POST':
        form = WriteTextForm(request.POST)
        if form.is_valid():
            text = form.save(commit=False)
            
            text.author_id = request.user.id

            text.save()
            return redirect('text:text_list')
    else:   
        form = WriteTextForm()

    return render(request, 'text/write_text.html', {'form': form})


def delete_text(request, text_id):
    author_id = Text.objects.get(id=text_id).author_id
    Text.objects.get(id=text_id).delete()
    return redirect('text:text_author', author_id)


def delete_comment(request, text_id, comment_id):
    Comment.objects.get(id=comment_id).delete()
    return redirect('text:text_detail', text_id)

def put_like(request, object_id, text_id, flag):

    #0 - list
    #1 - detail
    #2 - author
    #3 - comment
    type_obj = ContentType.objects.get_for_model(Text)
    if (flag == '3'):
        type_obj = ContentType.objects.get_for_model(Comment)

    if (len(Like.objects.filter(object_id=object_id, author_id = request.user.id, content_type=type_obj)) == 0):
        a = Like()
        a.author_id = request.user.id
        a.object_id = object_id
        a.content_type = type_obj
        a.save()
    
    likes = Like.objects.filter(object_id=object_id, content_type=type_obj).count()
    return JsonResponse({
        'like': likes,
    })

def write_comment(request, text_id):
    if request.method == 'POST':
        form = WriteCommentForm(request.POST)
       
        comment = form.save(commit=False)
                    
        comment.author_id = request.user.id
        comment.post_id = text_id

        comment.save()

        response_data = {}
        response_data['contents'] = comment.contents
        response_data['author'] = request.user.username
        response_data['author_id'] = request.user.id
        response_data['id'] = comment.id
        response_data['text_id'] = text_id
        response_data['created_date'] = comment.created_date.strftime("%d %B %Y г. %H:%M")


        return JsonResponse(response_data)

    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


def delete_like(request, object_id, text_id, flag):
    Like.objects.filter(author_id = request.user.id, object_id=object_id).first().delete()

    type_obj = ContentType.objects.get_for_model(Text)
    if (flag == '3'):
        type_obj = ContentType.objects.get_for_model(Comment)

    likes = Like.objects.filter(object_id=object_id, content_type=type_obj).count()
    return JsonResponse({
        'like': likes,
    })