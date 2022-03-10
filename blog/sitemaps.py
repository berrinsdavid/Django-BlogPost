from django.contrib.sitemaps import Sitemap
from .models import Post 

##creating a class 
class PostSiteMap(Sitemap):
    changefreg = 'weekly'
    priority = 0.9


    # desplaying last published 
    def items(self):
        return Post.published.all()
    
    ## Displaying last modified 
    def lastmod(self, obj):
        return obj.updated
