from django import template
from . . models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

register = template.Library()

@register.simple_tag
def total_posts():
    return Post.published.count()

## dispaling the lastest post on the
## they are displayed the sidebar 
@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count = 5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


## displaying the most commented post 
@register.simple_tag
##v creating a function that returns the most commented post
def get_most_commented_posts(count = 5):
    return Post.published.annotate(total_comments =Count('comments')).order_by ('-total_comments')[:count]


## Creating a markdown 
@register.filter(name = 'markdown')
## creating a function that counts the mumber of comments for each post 
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
