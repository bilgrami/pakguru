import json
from datetime import date, datetime, timedelta

from django.utils.text import slugify
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.cache import cache_page

from pakguru_app.models import Post, ShowFeed_HarvestJobLog

from .tasks import CacheTask, ProcessFeedsTask

FIVE_MINUTES = 60*5
ONE_DAY = 60*60*24
FOUR_HOURS = 60*60*4


@cache_page(FOUR_HOURS)
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
        post.channel_slug = slugify(post.show.channel)
        post.show_slug = slugify(post.show)
        post.label = post.title
        post.detail_url = reverse('post_detail',
                                  args=(post.channel_slug, post.show_slug,
                                        post.slug, post.post_id,))
        post.change_url = reverse('admin:pakguru_app_post_change',
                                  args=(post.post_id,))
        if post.extra_data and 'job_id' in post.extra_data:
            job_id = post.extra_data['job_id']
            post.feed_job_url = reverse('admin:pakguru_app_showfeed_harvestjoblog_change',  # noqa: E501
                                        args=(job_id,))
            post.feed_file_url = ShowFeed_HarvestJobLog.objects.get(pk=job_id).feed_data.url  # noqa: E501
        else:
            post.feed_job_url = 'javascript:void(0);'
            post.feed_file_url = 'javascript:void(0);'

        post.target_date += timedelta(hours=8)
        if post.show.host_name.lower() == 'unknown':
            post.show.host_name = None
        else:
            post.show.host_name = post.show.host_name + ' /'

        if post.show.total_shows < 0:
            post.show.total_shows = None
        else:
            post.show.total_shows = '/ Total: ' + str(post.show.total_shows)

        if post.show not in latest_posts:
            latest_posts[post.show] = posts.filter(show=post.show).order_by('-target_date').first()  # noqa: E501
        post.latest_post = latest_posts[post.show]
        if post.latest_post.target_date.date() >= yesterday:
            post.latest_post_color = 'text-danger'
        elif post.latest_post.target_date.date() >= two_days_ago:
            post.latest_post_color = 'text-warning'
        else:
            post.latest_post_color = 'text-info'

    return posts


@cache_page(FOUR_HOURS)
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
            'singleshowviewname': 'singletalkshow'
        }
    )


@cache_page(FOUR_HOURS)
def singletalkshow(request, channel, show, show_id):
    assert isinstance(request, HttpRequest)
    last_7_days = datetime.strftime(datetime.now() - timedelta(7), '%Y-%m-%d')
    posts = Post.objects.filter(is_active=True, target_date__gte=last_7_days, show__show_id=show_id).order_by('show__channel__name', 'show__name', '-target_date')  # noqa:E501
    posts = process_posts(posts)
    show_name = posts[0].show
    return render(
        request,
        'frontend_app/show_list.html',
        {
            'title': f'Episdoes of {show_name} Talk Show since last 7 days',
            "talkshows_page": "active",
            'message': show_name,
            'posts': posts
        }
    )


@cache_page(FOUR_HOURS)
def dramaserials(request):
    assert isinstance(request, HttpRequest)
    category = 'Drama Serials'
    posts = Post.objects.filter(is_active=True, category__name=category).order_by('show__channel__name', 'show__name', '-episode_number')  # noqa:E501
    posts = process_posts(posts)

    return render(
        request,
        'frontend_app/show_summary.html',
        {
            'title': 'Video List of Drama Serials',
            "dramaserials_page": "active",
            'message': 'Video List of Drama Serials',
            'posts': posts,
            'singleshowviewname': 'singledramaserial'
        }
    )


@cache_page(FOUR_HOURS)
def singledramaserial(request, channel, show, show_id):
    assert isinstance(request, HttpRequest)
    posts = Post.objects.filter(is_active=True, show__show_id=show_id).order_by('show__channel__name', 'show__name', '-target_date')  # noqa:E501
    process_posts(posts)
    show_name = posts[0].show

    return render(
        request,
        'frontend_app/show_list.html',
        {
            'title': f'Episdoes of {show_name} Drama Serial since last 7 days',
            "dramaserials_page": "active",
            'message': show_name,
            'posts': posts
        }
    )


@cache_page(FOUR_HOURS)
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
            'posts': posts
        }
    )


@cache_page(FOUR_HOURS)
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
            'posts': posts,
            'singleshowviewname': 'singlecomedyshow'
        }
    )


@cache_page(FOUR_HOURS)
def singlecomedyshow(request, channel, show, show_id):
    assert isinstance(request, HttpRequest)
    posts = Post.objects.filter(is_active=True, show__show_id=show_id).order_by('show__channel__name', 'show__name', '-target_date')  # noqa:E501
    posts = process_posts(posts)
    show_name = posts[0].show

    return render(
        request,
        'frontend_app/show_list.html',
        {
            'title': f'Episdoes of {show_name} Comedy show since last 7 days',
            "comedyshows_page": "active",
            'message': show_name,
            'posts': posts
        }
    )


@staff_member_required
def process_feeds(request):
    assert isinstance(request, HttpRequest)
    t = ProcessFeedsTask()
    result = t.process_feeds()
    data = {
        'Task': 'ProcessFeedsTask',
        'result': result
        }

    return JsonResponse(data)


def post_detail(request, channel, show, slug, post_id):
    assert isinstance(request, HttpRequest)
    posts = Post.objects.filter(is_active=True, post_id=post_id).all()  # noqa:E501
    posts = process_posts(posts)

    return render(
        request,
        'frontend_app/show_list.html',
        {
            'title': 'Show Post',
            "talkshows_page": "active",
            'message': posts[0].show,
            'posts': posts
        }
    )


@staff_member_required
def clear_cache(request):
    assert isinstance(request, HttpRequest)
    t = CacheTask()
    result, result_detail = t.clear_cache()
    data = {
        'Task': 'CacheTask - Clear',
        'result': result,
        'detail': result_detail
        }

    # data = json.dumps(data, indent=4)
    return JsonResponse(data, safe=False)


@staff_member_required
def get_cache(request):
    assert isinstance(request, HttpRequest)
    t = CacheTask()
    result, result_detail = t.get_cache()
    data = {
        'Task': 'CacheTask - Get',
        'result': result,
        'detail': result_detail
        }

    # data = json.dumps(data, indent=4)
    return JsonResponse(data, safe=False)
