
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
    data = []
    for post in posts:
        try:
            if len(post.text) > 40:
                urls = json.loads(str(post.text).replace('\'', '"'))
                utube = ''
                dailymotion = ''
                if 'www.youtube.com' in urls:
                    utube = urls['www.youtube.com']['link']
                if 'www.dailymotion.com' in urls:
                    dailymotion = urls['www.dailymotion.com']['link']
                post.description = dailymotion  #post.text
                post.name = utube  #post.text
            else:
                post.name = post.text
                post.description = post.text

            data.append(post)
        except Exception:
            post.name = post.text
            data.append(post)

    return render(
        request,
        'pakguru_app/dailytv.html',
        {
            'title': 'Daily TV',
            'message': 'Daily TV description goes here.',
            'year': datetime.now().year,
            'posts': data
        }
    )
