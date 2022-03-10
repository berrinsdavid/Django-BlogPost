from django.shortcuts import render, get_object_or_404
from .models import Post,Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from taggit.models import Tag

# Create your views here.
def post_list(request, tag_slug = None):
    posts = Post.published.all()
    tag = None 

    ##adding an if statements 
    if tag_slug:
        tag = get_object_or_404(Tag, slug = tag_slug)
        object_list =object_list.filter(tags__in=[tag])
    ## Adding pagination to the display page 
    object_list  = Post.published.all()
    paginator = Paginator (object_list,3) ## post in each page
    page = request.GET.get('page')

    #exceptiom 
    try:
        posts = paginator.page(page)
    

    except PageNotAnInteger:
        # if Page is not an integer deliver the  last page 
        posts = paginator.page(1)

    ## excepting an empty page 
    except EmptyPage:
        ## if the page is out of range then deliver the last page 
        posts = paginator.page(paginator.num_pages)
    return render(request,'blog/post/list.html',{ 'page': page,'posts': posts,'tag': tag})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,status='published',publish__year=year,publish__month=month,publish__day=day)

    # List of active comments for this Post 
    comments =post.comments.filter(active = True)
    new_comment = None 
    if request.method == 'POST':
        # A comment was posted 
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create a comment object But Don't save it into the database 
            new_comment = comment_form.save(commit = False)

            ## assign the current post to the comment current comment 
            new_comment.post = post 
            # save the comment into the database 
            new_comment.save()

    else:
        comment_form = CommentForm()
    return render(request,'blog/post/detail.html',{'post': post,'comments': comments,'new_comment': new_comment,'comment_form': comment_form})


#handling forms in a views 
def post_share(request, post_id):
    ## retrieve post by id 
    post = get_object_or_404(Post, id = post_id, status= 'published')
    sent = False

    # queryng
    if request.method  == "POST":
        # Form Was Submited 
        form = EmailPostForm(request.POST)

        if form.is_valid():
            #Form Fields Passed Validation 
            cd = form.cleaned_data
            post_url = request.build_absolute_url(post.get_absolute_url())
            subject = f"{cd['name']} Recommends you read ", f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n",f"{cd['name']}\'s  comments: {cd ['comments']}",
            sent_mail(subject, message, 'berringsdavid@mail.com', [cd['to']])
            sent = True


            # ...send Email 
    else:
        form = EmailPostForm()
    ##  adding some dictionaries 
    return render(request, 'blog/post/share.html', {'post': post,'form': form,'sent': sent})