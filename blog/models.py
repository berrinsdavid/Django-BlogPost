from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager


## creating a user models 
class PublishedManager(models.Manager):
    def get_querset(self):
        return super(PublishedManager,self).get_queryset().filter(status = 'published')

# Create your models here.
class Post(models.Model):
    STATUS_CHOICES =(
        ('draft','Draft'),
        ('published','published'),
    )
    title = models.CharField(max_length = 250)
    slug = models.SlugField(max_length = 250, unique_for_date ='publish')
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default = timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now = True)
    status = models.CharField(max_length = 10, choices = STATUS_CHOICES, default = 'draft')
    objects = models.Manager()
    published = PublishedManager()
    tags = TaggableManager()

    # creating a class meta
    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail',args=[ self.publish.year, self.publish.month, self.publish.day, self.slug])
## creating a model for comments in this blog 
class Comment(models.Model):
    post =  models.ForeignKey(Post, on_delete = models.CASCADE, related_name = 'comments')
    name = models.CharField(max_length = 80)
    email = models.EmailField()
    body = models. TextField()
    created = models.DateTimeField(auto_now_add= True)
    updated = models.DateTimeField(auto_now = True)
    active = models.BooleanField(default= True)


    ### creating a Meta class 
    class Meta:
        ordering = ('created',)

    ## creating a function for displaying comments in the database by their author 
    def __str__(self):
        return f'Comment by{self.name} on {self.post}'
