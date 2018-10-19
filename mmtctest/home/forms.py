'''from django import forms

from .models import Post

class PostForm(forms.ModelForm):

    class Meta:
        model = Post 
        fields = ('source', 'dest',)'''

from django import forms

from .models import Post2

class PostForm(forms.ModelForm):

    class Meta:
        model = Post2 
        fields = ('source', 'dest', 'date',)