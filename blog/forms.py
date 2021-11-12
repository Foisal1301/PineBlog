from django import forms
from .models import Post,Category,Comment,Reply

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title','category','author','body','header_image')#'snippet'

        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'category':forms.Select(attrs={'class':'form-select'}),
            'author': forms.TextInput(attrs={'class': 'form-control','id':'author','type':'hidden'}),
            'body':forms.Textarea(attrs={'class':'form-control'}),
            #'snippet':forms.Textarea(attrs={'class':'form-control'}),
        }

class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title','category','body',)

        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'category':forms.Select(attrs={'class':'form-select'}),
            'body':forms.Textarea(attrs={'class':'form-control'}),
        }

class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

        widgets = {
            #'name':forms.Select(attrs={'class':'form-select'}),
            'body':forms.Textarea(attrs={'class':'form-control'}),
        }

class AddReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ('body',)

        widgets = {
            #'name':forms.Select(attrs={'class':'form-select'}),
            'body':forms.Textarea(attrs={'class':'form-control'}),
        }

class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

        widgets = {'name':forms.TextInput(attrs={'class':'form-control'}),}
