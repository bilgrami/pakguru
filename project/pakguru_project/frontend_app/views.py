
import json
from datetime import datetime

from django.http import HttpRequest
from django.shortcuts import render

from pakguru_app.models import Post


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'pakguru_app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )


def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'pakguru_app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )


def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'pakguru_app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )


def dailytv(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    posts = Post.objects.filter(is_active=True).all().order_by('-post_id')
    # data = {}
    # for post in posts:
    #     d = {}
    #     d['post_id'] = post.post_id
    #     d['title'] = post.title
    #     urls = json.loads(post.text.replace('\'', '"'))
    #     link = ''
    #     if 'www.youtube.com' in urls:
    #         link = urls['www.youtube.com']['link']
    #     d['link'] = link
    #     data[post.post_id] = d

    return render(
        request,
        'pakguru_app/dailytv.html',
        {
            'title': 'Daily TV',
            'message': 'Daily TV description goes here.',
            'year': datetime.now().year,
            'posts': posts
        }
    )
