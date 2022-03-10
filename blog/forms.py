from django import forms 
from .models import Comment


## creating a class 
class EmailPostForm(forms.Form):
    name = forms.CharField(max_length = 25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required = False,widget = forms.Textarea)

# creating a comment  Form by using the comment models 

class CommentForm(forms.ModelForm):
    ## creating a meta class 
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')