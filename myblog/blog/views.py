from django.shortcuts import render

# Create your views here.
from .models import Post
from django.http import Http404
from django.shortcuts import get_object_or_404 # function instead error DoesNotExist
from django.core.paginator import Paginator # Page making
from django.core.paginator import EmptyPage, \
                                  PageNotAnInteger


def post_list(request):
    post_list = Post.published.all()
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page',1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # Если page_number не число, не целое число
        # Вернем первую страницу
        posts = paginator.page(1)
    except EmptyPage:
        # Если page_number вне диапазона
        # Вернем последнюю страницу
        posts = paginator.page(paginator.num_pages)
    
    return render(
        request,
        'blog/post/list.html',
        {'posts': posts}
    ) 

def post_detail(request, year, month, day, post):
    # try:      # Do not use get_object_or_404
    #     post = Post.published.get(id=id)
    # except Post.DoesNotExist:
    #     raise Http404('No Post found.')
    post = get_object_or_404(
                                Post,
                                status=Post.Status.PUBLISHED,
                                slug=post,
                                publish__year=year,
                                publish__month=month,
                                publish__day=day 
                            )
    return render(
                request,
                'blog/post/detail.html',
                {'post':post}
                )