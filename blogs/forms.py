from django import forms
from .models import blog_post, Comment, Tag
from ckeditor.widgets import CKEditorWidget

class BlogPostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = blog_post
        fields = ['title', 'content', 'image', 'category', 'tags']
        widgets = {
            'tags': forms.SelectMultiple(attrs={'id': 'id_tags'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tags'].queryset = Tag.objects.none()

        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['tags'].queryset = Tag.objects.filter(category_id=category_id).order_by('name')
            except (ValueError, TypeError):
                pass  
        elif self.instance.pk:
            self.fields['tags'].queryset = self.instance.category.tags.order_by('name')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget.attrs.update({'rows': 1, 'placeholder': 'Comment'})
