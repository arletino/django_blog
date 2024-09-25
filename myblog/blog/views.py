from django.shortcuts import render

# Create your views here.
from .models import Post
from django.http import Http404
from django.shortcuts import get_object_or_404 # function instead error DoesNotExist
from django.core.paginator import Paginator # Page making
from django.core.paginator import EmptyPage, \
                                  PageNotAnInteger

from .models import Post
from django.views.generic import ListView
from .forms import EmailPostForm # Форма для отправки по почте
from django.core.mail import send_mail
from django.db.models import Count # Агрегирующая функция из модуля models

from django.contrib.postgres.search import SearchVector # Поиск по нескольким полям
from .forms import EmailPostForm, CommentForm, SearchForm # Реализация поиска

class PostListView(ListView):
    '''
        Альтернативное представление списка постов
        на основе классов  
    '''
    queryset = Post.published.all() # имеем конкретный набор запросов QuerySet, 
    # не извлекая все объекты 
    # model = Post # Альтернатива queryset 
    # Django сформирует  типовой набор запросов Post.object.all()
    context_object_name = 'posts'
    paginate_by = 3 # По страничная разбивка вывода
    template_name = 'blog/post/list.html' 

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
        # Список активных комментариев к этому посту
        comments = post.comments.filter(active=True)
        # Форма для комментирования 
        form = CommentForm()
        # Список схожих постов
        post_tags_ids = post.tags.values_list('id', flat=True)
        similar_posts = Post.published.filter(tags__in=post_tags_ids)\
                                      .exclude(id=post.id)
        similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
                                      .order_by('-same_tags','-publish')[:4]
        return render(
                    request,
                    'blog/post/detail.html',
                    {'post':post,
                     'comments':comments,
                     'form':form,
                     'similar_posts': similar_posts
                     }
                    )
    
    def post_share(request, post_id):
        post = get_object_or_404(
            Post,
            id=post_id,
            status=Post.Status.PUBLISHED
        )
        sent = False 

        if request.method == 'POST':
            form = EmailPostForm(request.POST)
            # from.errors   # Получить ошибки валидации формы
            if form.is_valid():
                cd = form.cleaned_data # Получение данных формы
                post_url = request.build_absolute_uri(
                    post.get_absolute_url()
                )
                subject = f'{cd['name']} recommends you read' \
                          f'{post.title}'
                message = f'Read {post.title} at {post_url}\n\n' \
                          f"{cd['name']}\'s comments: {cd['comments']}"
                send_mail(
                    subject, 
                    message, 
                    'account@gmail.com',
                          [cd['to']]
                          )
                send = True
        else:
            form = EmailPostForm()
        return render(request, 'blog/post/share.html', {'post':post,
                                                        'form':form,
                                                        'sent':sent})

from django.views.decorators.http import require_POST
from .forms import CommentForm    

@require_POST 
def post_comment(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )
    comment = None
    # Комментарий был отправлен
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Создаем объект класс Comment, не сохраняя его в базе данных
        # Позволяет изменить объект перед добавлением в базу
        comment = form.save(commit=False)
        # Назначаем пост комментарию
        comment.post = post
        # Сохраняем комментарий в базе
        comment.save()
    return render(request, 
                  'blog/post/comment.html',
                  {'post':post,
                   'form':form,
                   'comment':comment}
                  )

from taggit.models import Tag


def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
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
        {'posts': posts,
         'tag': tag}
    )

def post_search(request):
    '''Полнотекстовый поиск по полям 'title', 'body' '''
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.published.annotate(
                search=SearchVector('title', 'body'),
            ).filter(search=query)
    return render(
        request,
        'blog/post/search.html',
        {'form': form,
         'query': query,
         'results': results}
    )
  