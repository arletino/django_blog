from django import template # Иммпорт шаблона
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe # Для отмены экранирования данных в шаблон
import markdown

register = template.Library()


@register.simple_tag # Регистрация тега
def total_posts():
    return Post.published.count()

@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}

@register.simple_tag 
def get_most_commented_posts(count=5):
    return Post.published.annotate(        # формируем набор запросов
        total_comments = Count('comments')
    ).order_by('-total_comments')[:count]

@register.filter(name='markdown')    # Регистрация Шаблонного фильтра
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
