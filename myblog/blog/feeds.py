# Новостная лента

import markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy
from .models import Post


class LatestPostsFeed(Feed):
    title = 'My blog'
    link = reverse_lazy('blog:post_list')
    description = 'New posts of my blog.'

    def items(self):
        return Post.published.all()[:5] # Берем последние 5 публикаций
    
    def item_title(self, item):
        return item.title             # Возвращает название публикации
    
    def item_description(self, item):

        '''Возвращает обрезанное тело в стиле Маркдаун'''

        return truncatewords_html(markdown.markdown(item.body), 30)  
    
    def item_pubdate(self, item):
        ''''''
        return item.publish