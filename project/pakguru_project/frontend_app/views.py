import json
from datetime import datetime, timedelta

from django.http import HttpRequest
from django.shortcuts import render
from django.views.decorators.cache import cache_page

from pakguru_app.models import Post


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'pakguru_app/index.html',
        {
            'title': 'Home Page',
            'year': datetime.now().year,
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

@cache_page(24*60*4)
def dailytv(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    yesterday = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
    posts = Post.objects.filter(is_active=True, target_date__gte=yesterday, category__name='Talk Shows').all().order_by('-target_date', 'show__channel__name', 'show__name')  # noqa:E501
    for post in posts:
        try:
            utube = ''
            dailymotion = ''
            if len(post.text) > 40:
                urls = json.loads(str(post.text).replace('\'', '"'))
                if 'www.youtube.com' in urls:
                    utube = urls['www.youtube.com']['link']
                if 'www.dailymotion.com' in urls:
                    dailymotion = urls['www.dailymotion.com']['link']

                # post.description = dailymotion  #post.text
                post.name = dailymotion if dailymotion else utube  #post.text
            else:
                post.name = post.text
                post.description = post.text

        except Exception:
            post.name = post.text
        
        post.url = post.name.replace("watch", 'embed')
        if 'www.youtube.com' in post.url:
            utube = post.url
        if 'www.dailymotion.com' in post.url:
            dailymotion = post.url
        post.type = 'dailymotion' if dailymotion else 'utube'
        post.label = post.title
        dates = [posts.order_by('target_date').values_list('target_date', flat=True).distinct('target_date')]

    return render(
        request,
        'pakguru_app/dailytv.html',
        {
            'title': 'Daily TV',
            'message': 'Daily TV description goes here.',
            'year': datetime.now().year,
            'today': datetime.now().date,
            'dates': dates,
            'posts': posts
        }
    )
