import json
from datetime import datetime, timedelta, date

import django.utils.text
from django.http import HttpRequest
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.cache import cache_page

from pakguru_app.models import Post, ShowFeed_HarvestJobLog
FIVE_MINUTES = 60*5
ONE_DAY = 60*60*24


@cache_page(ONE_DAY)
def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'pakguru_app/index.html',
        {
            'title': 'Home Page',
            "home_page": "active",
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
            'title': '',
            'message': '',
            'year': datetime.now().year,
        }
    )


@cache_page(ONE_DAY)
def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'pakguru_app/about.html',
        {
            'title': 'About',
            'message': 'Pak.guru is a listing of Daily Talk-shows and Dramas.',
            'year': datetime.now().year,
        }
    )


def get_post_url(url_text):
    # utube = ''
    dailymotion = ''
    if type(url_text) is dict or "{'" in url_text:
        urls = json.loads(str(url_text).replace('\'', '"'))
        if 'www.youtube.com' in urls:
            url = urls['www.youtube.com']['link']
        if 'www.dailymotion.com' in urls:
            url = urls['www.dailymotion.com']['link']
    else:
        url = url_text

    url = url.replace("watch", 'embed')
    url = url.replace("http://", 'https://')
    # if 'www.youtube.com' in url:
    #     utube = url
    if 'www.dailymotion.com' in url:
        dailymotion = url
    post_type = 'dailymotion' if dailymotion else 'utube'
    return (post_type, url)


def process_posts(posts):
    latest_posts = {}
    yesterday = date.today() - timedelta(days=1)
    two_days_ago = date.today() - timedelta(days=2)
    # TODO: need to handle DST transition
    time_in_pakistan = date.today() + timedelta(hours=12)

    for post in posts:
        post.type, post.url = get_post_url(post.text)
        post.channel_slug = django.utils.text.slugify(post.show.channel)
        post.show_slug = django.utils.text.slugify(post.show)
        post.label = post.title
        post.change_url = reverse('admin:pakguru_app_post_change',
                                  args=(post.post_id,))
        job_id = post.extra_data['job_id']
        post.feed_job_url = reverse('admin:pakguru_app_showfeed_harvestjoblog_change',  # noqa: E501
                                    args=(job_id,))
        post.feed_file_url = ShowFeed_HarvestJobLog.objects.get(pk=job_id).feed_data.url  # noqa: E501
        if post.show not in latest_posts:
            latest_posts[post.show] = Post.objects.filter(show=post.show).order_by('-target_date').first()  # noqa: E501

        post.latest_post = latest_posts[post.show]
        post.time_in_pakistan = time_in_pakistan
        if post.latest_post.target_date >= yesterday:
            post.latest_post_color = 'text-danger'
        elif post.latest_post.target_date >= two_days_ago:
            post.latest_post_color = 'text-warning'

    return posts


@cache_page(FIVE_MINUTES)
def talkshows(request):
    category = 'Talk Shows'
    assert isinstance(request, HttpRequest)
    last_7_days = datetime.strftime(datetime.now() - timedelta(7), '%Y-%m-%d')
    posts = Post.objects.filter(is_active=True, target_date__gte=last_7_days, category__name=category).all().order_by('show__channel__name', 'show__name', '-target_date')  # noqa:E501
    process_posts(posts)

    return render(
        request,
        'pakguru_app/talkshows.html',
        {
            'title': 'Daily Talk Shows',
            "talkshows_page": "active",
            'category': category,
            'message': 'Daily Talk shows',
            'posts': posts,
            'posts_visible': False
        }
    )


@cache_page(FIVE_MINUTES)
def singletalkshow(request, channel, show, show_id):
    category = 'Talks Shows'
    assert isinstance(request, HttpRequest)

    last_7_days = datetime.strftime(datetime.now() - timedelta(7), '%Y-%m-%d')
    posts = Post.objects.filter(is_active=True, target_date__gte=last_7_days, show__show_id=show_id).order_by('show__channel__name', 'show__name', '-target_date')  # noqa:E501
    process_posts(posts)

    return render(
        request,
        'pakguru_app/talkshows.html',
        {
            'title': 'Daily Talk Show',
            "talkshows_page": "active",
            'category': category,
            'message': 'Daily Talk show',
            'posts': posts,
            'posts_visible': True
        }
    )


@cache_page(FIVE_MINUTES)
def dramaserials(request):
    category = 'Drama Serials'
    assert isinstance(request, HttpRequest)
    posts = Post.objects.filter(is_active=True, category__name=category).order_by('show__channel__name', 'show__name', '-target_date')  # noqa:E501
    process_posts(posts)

    return render(
        request,
        'pakguru_app/dramaserials.html',
        {
            'title': 'Drama Serials',
            "dramaserials_page": "active",
            'category': category,
            'message': 'Drama Serials',
            'posts': posts,
            'posts_visible': False
        }
    )


@cache_page(FIVE_MINUTES)
def singledramaserial(request, channel, show, show_id):
    category = 'Drama Serials'
    assert isinstance(request, HttpRequest)
    posts = Post.objects.filter(is_active=True, show__show_id=show_id).order_by('show__channel__name', 'show__name', '-target_date')  # noqa:E501
    process_posts(posts)

    return render(
        request,
        'pakguru_app/dramaserials.html',
        {
            'title': 'Drama Serial',
            "dramaserials_page": "active",
            'category': category,
            'message': 'Drama Serials',
            'posts': posts,
            'posts_visible': True
        }
    )
