from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy
from .models import Post 

## Adding a class 
class LatestPostsFeed(Feed):
    title = 'My Articles'
    link = reverse_lazy('blog:post_list')
    description = 'New Post Of My Blog'

    ## defining of functions 
    def items(self):
        return Post.published.all()[:5]

    def item_title(self,item):
        return item.title

    def item_description(self,item):
        return truncatewords(item.body, 30)