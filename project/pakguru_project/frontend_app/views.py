import json
from datetime import date, datetime, timedelta

import django.utils.text
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.cache import cache_page

from pakguru_app.models import Post, ShowFeed_HarvestJobLog

from .tasks import ProcessFeedTask

FIVE_MINUTES = 60*5
ONE_DAY = 60*60*24
FOUR_HOURS = 60*60*4


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
        if post.latest_post.target_date >= yesterday:
            post.latest_post_color = 'text-danger'
        elif post.latest_post.target_date >= two_days_ago:
            post.latest_post_color = 'text-warning'

    return posts


@cache_page(FIVE_MINUTES)
def talkshows(request):
    assert isinstance(request, HttpRequest)
    category = 'Talk Shows'
    last_7_days = datetime.strftime(datetime.now() - timedelta(7), '%Y-%m-%d')
    posts = Post.objects.filter(is_active=True, target_date__gte=last_7_days, category__name=category).all().order_by('show__channel__name', 'show__name', '-target_date')  # noqa:E501
    posts = process_posts(posts)

    return render(
        request,
        'frontend_app/show_summary.html',
        {
            'title': 'Video List of Daily Talk Shows',
            "talkshows_page": "active",
            'message': 'Video List of Daily Talk Shows',
            'posts': posts,
            'posts_visible': False
        }
    )


@cache_page(FIVE_MINUTES)
def singletalkshow(request, channel, show, show_id):
    assert isinstance(request, HttpRequest)
    last_7_days = datetime.strftime(datetime.now() - timedelta(7), '%Y-%m-%d')
    posts = Post.objects.filter(is_active=True, target_date__gte=last_7_days, show__show_id=show_id).order_by('show__channel__name', 'show__name', '-target_date')  # noqa:E501
    posts = process_posts(posts)

    return render(
        request,
        'frontend_app/show_list.html',
        {
            'title': 'Daily Talk Show',
            "talkshows_page": "active",
            'message': posts[0].show,
            'posts': posts
        }
    )


@cache_page(FIVE_MINUTES)
def dramaserials(request):
    assert isinstance(request, HttpRequest)
    category = 'Drama Serials'
    posts = Post.objects.filter(is_active=True, category__name=category).order_by('show__channel__name', 'show__name', '-target_date')  # noqa:E501
    posts = process_posts(posts)

    return render(
        request,
        'frontend_app/show_summary.html',
        {
            'title': 'Video List of Drama Serials',
            "dramaserials_page": "active",
            'message': 'Video List of Drama Serials',
            'posts': posts
        }
    )


@cache_page(FIVE_MINUTES)
def singledramaserial(request, channel, show, show_id):
    assert isinstance(request, HttpRequest)
    posts = Post.objects.filter(is_active=True, show__show_id=show_id).order_by('show__channel__name', 'show__name', '-target_date')  # noqa:E501
    process_posts(posts)

    return render(
        request,
        'frontend_app/show_list.html',
        {
            'title': 'Drama Serial Video',
            "dramaserials_page": "active",
            'message': posts[0].show,
            'posts': posts
        }
    )


@cache_page(FIVE_MINUTES)
def recentshows(request):
    assert isinstance(request, HttpRequest)
    yesterday = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
    posts = Post.objects.filter(is_active=True, publish_date__gte=yesterday).order_by('-post_id')  # noqa:E501
    posts = process_posts(posts)

    return render(
        request,
        'frontend_app/show_list.html',
        {
            'title': 'Recently Published Videos',
            "recentshows_page": "active",
            'message': 'Recently Published Videos',
            'posts': posts[:50]
        }
    )


@cache_page(FIVE_MINUTES)
def comedyshows(request):
    assert isinstance(request, HttpRequest)
    category = 'Comedy Shows'
    posts = Post.objects.filter(is_active=True, category__name=category).order_by('show__channel__name', 'show__name', '-target_date')  # noqa:E501
    posts = process_posts(posts)

    return render(
        request,
        'frontend_app/show_summary.html',
        {
            'title': 'Video list of Comedy Shows',
            "comedyshows_page": "active",
            'message': 'Video list of Comedy Shows',
            'posts': posts
        }
    )


@cache_page(FIVE_MINUTES)
def singlecomedyshow(request, channel, show, show_id):
    assert isinstance(request, HttpRequest)
    posts = Post.objects.filter(is_active=True, show__show_id=show_id).order_by('show__channel__name', 'show__name', '-target_date')  # noqa:E501
    posts = process_posts(posts)

    return render(
        request,
        'frontend_app/show_list.html',
        {
            'title': 'Comedy Show Videos',
            "comedyshows_page": "active",
            'message': posts[0].show,
            'posts': posts
        }
    )


@staff_member_required
def process_feeds(request, param1="True", param2=0, param3=-1):
    t = ProcessFeedTask()
    result = t.process_feeds(param1, param2, param3)
    data = {
        'params':
            {
                'param1': param1,
                'param2': param2,
                'param3': param3
            },
        'result': result
        }

    # just return a JsonResponse
    return JsonResponse(data)
